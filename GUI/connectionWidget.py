import sys
from PySide2.QtWidgets import QWidget, QComboBox, QPushButton, QApplication, QHBoxLayout, QMainWindow
from PySide2.QtCore import Qt
from PySide2 import QtCore
import serial
import serial.tools.list_ports
from messageBox import errorBox
import time
import struct

# Adapted from https://github.com/Wauro21/bssc/tree/main/gui

class connectionWidget(QWidget):
	# Class Signals
	connect_signal = QtCore.Signal()
	disconnect_signal = QtCore.Signal()

	def __init__(self, main_wdw: QMainWindow, parent=None):
		super().__init__(parent)

		# Variables
		self.serial_COM = None
		self.main_wdw = main_wdw
		self.config = self.main_wdw.config
		
		# Widgets 
		self.serial_ports_cbox = QComboBox()
		self.serial_ports_cbox.setToolTip('Available serial ports')
		self.refresh_btn = QPushButton('Refresh') # refresh COMs
		self.refresh_btn.setToolTip('Update available serial ports ')
		self.connect_btn = QPushButton('Connect')

		self.connect_btn.setMinimumWidth(96)

		# Init routines
		self.serialList()
		self.connect_btn.setToolTip('Send initialisation parameters and \nreceive acknowledgment message')

		# Signals and slots
		self.refresh_btn.clicked.connect(self.serialList)
		self.connect_btn.clicked.connect(self.connectionHandler)

		# Widget Layout
		layout = QHBoxLayout()
		layout.addWidget(self.serial_ports_cbox)
		layout.addWidget(self.refresh_btn)
		layout.addWidget(self.connect_btn)

		self.setLayout(layout)


	def serialList(self):
		# Clear combobox 
		self.serial_ports_cbox.clear()

		# Get list of available ports
		show_ports = []
		ports = serial.tools.list_ports.comports()
		for port, _, _ in sorted(ports):
			show_ports.append(port)

		# If no ports found, disable connect button
		if(len(show_ports) == 0):
			self.connect_btn.setEnabled(False)
			return
		else:
			# Add ports to combobox
			self.serial_ports_cbox.addItems(show_ports)
			# Enable connect button
			self.connect_btn.setEnabled(True)


	def connectionHandler(self):
		port = self.serial_ports_cbox.currentText()
		if port == None: # port == None
			# No port is selected
			raise Exception('No port selected') 
		try:
			if self.serial_COM: # != None
				self.serial_COM.close()
				self.serial_COM = None
				self.disconnect_signal.emit()
				connect_btn_text = 'Connect'
				self.connect_btn.setToolTip('Send initialisation parameters and \nreceive acknowledgment message')
				port_list_refresh_enable = True
			else:
				self.serial_COM = serial.Serial(port, baudrate=self.config.dict['serial']['baudrate'], timeout=self.config.dict['serial']['timeout'])
				self.connectionTest()
				self.connect_signal.emit()
				connect_btn_text = 'Disconnect'
				self.connect_btn.setToolTip('Set serial port to <b>None</b>')
				port_list_refresh_enable = False
			self.connect_btn.setText(connect_btn_text)
			self.serial_ports_cbox.setEnabled(port_list_refresh_enable)
			self.refresh_btn.setEnabled(port_list_refresh_enable)

		except Exception as e:
			self.serial_COM.close()
			self.serial_COM = None
			self.serial_ports_cbox.setEnabled(True)
			self.refresh_btn.setEnabled(True)
			show_error = errorBox(e, self)
			show_error.exec_()

	def connectionTest(self):
		azim_id = self.config.dict['resolutions']['default_azim']
		elev_id = self.config.dict['resolutions']['default_elev']
		Nrev_azim = self.config.dict['resolutions']['list'][azim_id]
		Nrev_azim = int(360 / Nrev_azim)
		Nrev_elev = self.config.dict['resolutions']['list'][elev_id]
		Nrev_elev = int(360 / Nrev_elev)

		Pa = self.config.dict['default_params']['Pa']
		Tas_azim = self.config.dict['default_params']['delays'][azim_id]['Tas']
		Tai_azim = self.config.dict['default_params']['delays'][azim_id]['Tai']
		Tas_elev = self.config.dict['default_params']['delays'][elev_id]['Tas']
		Tai_elev = self.config.dict['default_params']['delays'][elev_id]['Tai']

		out_str = f'c-{Nrev_azim}-{Pa}-{Tas_azim}-{Tai_azim}-{Nrev_elev}-{Pa}-{Tas_elev}-{Tai_elev}\n'

		if self.config.dict['debug_print']:
			print(out_str[:-1])
			
		self.serial_COM.write(out_str.encode())
		time.sleep(0.10) # seconds
		response = self.serial_COM.readline() # Change to receive mode, Arduino sends \n to terminate
		response = str(response,'utf-8').rstrip()
		# print(response)
		if (response == 'ack'):
			return True
		else:
			raise Exception('Device did not respond')

	def send2COM(self, string: str):
		self.serial_COM.write(string.encode())

	def receiveOnlyCOM(self):
		time.sleep(0.10)
		received_string = self.serial_COM.readline()  
		received_string = str(received_string,'utf-8').rstrip() 
		return received_string

	def receiveBytesCOM(self):
		time.sleep(0.10)
		# received = self.serial_COM.readline() # This caused problems when '\n' is contained within the data
		received = self.readLine(self.serial_COM)
		return received

	# Adapted from https://stackoverflow.com/questions/16470903/pyserial-2-6-specify-end-of-line-in-readline
	def readLine(self, a_serial, eol = b'\n\n\n'):
		len_eol = len(eol)
		line = bytearray()
		size_of_int = 4
		while True:
			c = a_serial.read(size_of_int) # read (size_of_int) bytes
			if c:
				line += c
				if line[-(len_eol+1):] == b'r'+eol or line[-(len_eol+1):] == b'l'+eol:
					break
			else:
				break
		return line

	def unpackDataBytes(self, data: str):
		size_of_int = 4
		size_of_char = 1
		size_of_float = 4

		# compute amount of int data
		n_int = 4
		n_int_str = 'i'*n_int #'iiii'

		# compute amount of char data
		n_char = 4
		n_char_str = 'c'*n_char #'cccc', 'r\n\n\n' or 'l\n\n\n'

		# compute amount of float data
		n_float = int(len(data) - n_int*size_of_int - n_char*size_of_char) # extract metadata. Last char is \n
		n_float = int(n_float/size_of_float)
		# n_float_str = 'f'*n_float
		n_float_str = 'i'*n_float # Changed serial write of ADC data from float to int (10 bit, 0->1023)
								  # Size of float is the same as Size of int	

		values_tuple = struct.unpack(n_float_str + n_int_str + n_char_str, data) #returns tuple

		mean_time = values_tuple[-6-2] #microseconds
		mean_time_total = values_tuple[-5-2] #microseconds
		angle = values_tuple[-4-2]
		steps_to_move = values_tuple[-3-2]
		direction_char = str(values_tuple[-2-2], 'utf-8')
		float_tuple = values_tuple[0:-6-2]  #remove last elements
		float_list = list(float_tuple)

		return angle, direction_char, float_list, mean_time, mean_time_total
	

if __name__ == '__main__':
	app = QApplication([])
	widget = connectionWidget()
	widget.show()
	sys.exit(app.exec_())