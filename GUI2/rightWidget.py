import sys
import time
from PySide2.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout, QFormLayout, QVBoxLayout, QRadioButton, QDoubleSpinBox, QSpinBox, QComboBox, QLabel
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon, QPixmap
import PySide2.QtCore
from math import floor

import numpy as np

# Constants for operation
# -> Angle parameters: degree
LOWEST_DEG = 0 
HIGHEST_DEG = 360*40  # 40 revs
STEP_INCREMENT = 10
USE_DECIMALS = 2
DEG_UNITS = 'º' 

# -> Pa parameters: steps
LOWEST_PA = 0 
HIGHEST_PA = 10000
STEP_INCREMENT = 10
PA_UNITS = ' step'

# -> Time parameters: microseconds
MIN_TIME_STEP = 0 # us
MAX_TIME_STEP = 2000 # us
TIME_STEP_INCREMENT = 10
TIME_UNITS = ' \u03BCs'

STATUS_BAR_TIMEOUT = 5000

class rightWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.font_dict = {
					"family" : "Segoe UI",
					"title_size" : 14
					}      
		#---------------------------------------------
		# Objects
		self.csv_flag = True

		#---------------------------------------------
		# Widgets       
		# -> Labels
		self.azimuth_txt = QLabel('<b>Azimuth Settings</b>')
		self.azimuth_txt.setStyleSheet(f"font : {self.font_dict['title_size']}pt '{self.font_dict['family']}';")
		self.azimuth_img = QLabel()
		self.img = QPixmap('img/azimuth.png')
		self.img = self.img.scaled(250, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
		self.azimuth_img.setPixmap(self.img)

		self.elevation_txt = QLabel('<b>Elevation Settings</b>')
		self.elevation_txt.setStyleSheet(f"font : {self.font_dict['title_size']}pt '{self.font_dict['family']}';")
		self.elevation_img = QLabel()
		self.img = QPixmap('img/elevation.png')
		self.img = self.img.scaled(250, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
		self.elevation_img.setPixmap(self.img)

		# -> Combo boxes
		self.Nrev_combo = QComboBox()
		self.Nrev_list = ['1.8 degree/step','0.9 degree/step','0.45 degree/step','0.225 degree/step','0.1125 degree/step','0.05625 degree/step']
		self.Nrev_combo.addItems(self.Nrev_list)

		# -> Spin boxes
		self.Pa_spinbox = QSpinBox()
		self.Tas_spinbox = QSpinBox()
		self.Tai_spinbox = QSpinBox()
		self.angle_spinbox = QDoubleSpinBox()

		# -> Radio buttons
		self.a_radio = QRadioButton()
		self.l_radio = QRadioButton()
		self.r_radio = QRadioButton()

		self.a_radio.setIcon(QIcon('img/protractor.png'))
		self.a_radio.setIconSize(QSize(90,60))
		self.a_radio.setFixedSize(90,60)
		self.a_radio.setToolTip('Move to an <b>absolute</b> angle')

		self.l_radio.setIcon(QIcon('img/counterclockwise.png'))
		self.l_radio.setIconSize(QSize(90,60))
		self.l_radio.setFixedSize(90,60)
		self.l_radio.setToolTip('Move <b>counterclockwise</b>')

		self.r_radio.setIcon(QIcon('img/clockwise.png'))
		self.r_radio.setIconSize(QSize(90,60))
		self.r_radio.setFixedSize(90,60)
		self.r_radio.setToolTip('Move <b>clockwise</b>')

		# -> Bottom buttons
		self.move_btn = QPushButton('Move')
		self.reset_btn = QPushButton('Reset angle')
		self.default_btn = QPushButton('Default')
		self.apply_btn = QPushButton('Apply')

		self.move_btn.setToolTip('Rotate stepper motor')
		self.reset_btn.setToolTip('Set current position as initial angle')

		#---------------------------------------------
		# Init routine 
		self.angleBoxConfig(self.angle_spinbox)
		self.a_radio.setChecked(True)

		self.Nrev_combo.setCurrentText(self.Nrev_list[5])
		self.NBoxConfig(self.Pa_spinbox)
		self.TimeBoxConfig(self.Tai_spinbox)
		self.TimeBoxConfig(self.Tas_spinbox)

		# Objects
		self.param_dict = self.getFieldsValues()

		#---------------------------------------------
		# Signals and slots
		self.move_btn.clicked.connect(self.sendMovement)
		self.reset_btn.clicked.connect(self.sendReset)

		self.default_btn.clicked.connect(self.resetParameters)
		self.apply_btn.clicked.connect(self.sendParameters)
		self.connect(self.Nrev_combo, PySide2.QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.resetParameters)

		#---------------------------------------------
		# Layout
		v_layout = QVBoxLayout()

		# -> Title Label AZIMUTH
		h_layout = QHBoxLayout()
		h_layout.addWidget(self.azimuth_img)
		h_layout.addWidget(self.azimuth_txt)
		h_layout.addStretch()
		v_layout.addLayout(h_layout)

		# -> Resolution and Acceleration parameters
		param_fields = QFormLayout()
		param_fields.addRow('Azimuth resolution', self.Nrev_combo)
		param_fields.addRow('Acceleration period', self.Pa_spinbox)
		param_fields.addRow('Maximum added delay', self.Tas_spinbox)
		param_fields.addRow('Minimum added delay', self.Tai_spinbox)
		v_layout.addLayout(param_fields)
		# Resolution and Acceleration buttons
		btn_row = QHBoxLayout()
		btn_row.addWidget(self.default_btn)
		btn_row.addWidget(self.apply_btn)
		v_layout.addLayout(btn_row)

		# -> Angle SETTINGS
		angle_fields = QFormLayout()
		angle_fields.addRow('Angle', self.angle_spinbox)
		v_layout.addLayout(angle_fields)
		# -> Radio buttons (a, l, r)
		radio_btn_row = QHBoxLayout()
		radio_btn_row.addWidget(self.a_radio)
		radio_btn_row.addWidget(self.l_radio)
		radio_btn_row.addWidget(self.r_radio)
		v_layout.addLayout(radio_btn_row)
		# -> Bottom buttons
		btn_row = QHBoxLayout()
		btn_row.addWidget(self.move_btn)
		btn_row.addWidget(self.reset_btn)
		v_layout.addLayout(btn_row)


		# -> Title Label ELEVATION
		h_layout = QHBoxLayout()
		h_layout.addWidget(self.elevation_img)
		h_layout.addWidget(self.elevation_txt)
		h_layout.addStretch()
		v_layout.addLayout(h_layout)

		self.setLayout(v_layout)

	#---------------------------------------------
	def angleBoxConfig(self, box):
		box.setMinimum(LOWEST_DEG)
		box.setMaximum(HIGHEST_DEG)
		box.setSingleStep(STEP_INCREMENT)
		box.setSuffix(DEG_UNITS)

	def NBoxConfig(self, box):
		box.setMinimum(LOWEST_PA)
		box.setMaximum(HIGHEST_PA)
		box.setSingleStep(STEP_INCREMENT)
		box.setSuffix(PA_UNITS)

	def TimeBoxConfig(self,box):
		box.setMinimum(MIN_TIME_STEP)
		box.setMaximum(MAX_TIME_STEP)
		box.setSingleStep(TIME_STEP_INCREMENT)
		box.setSuffix(TIME_UNITS)

	#---------------------------------------------
	def getFieldsValues(self):
		ret_dict = {
			'Nrev':int(360/float(self.Nrev_combo.currentText().split()[0])),
			'Pa':self.Pa_spinbox.value(),
			'Tas':self.Tas_spinbox.value(),
			'Tai':self.Tai_spinbox.value()
		}
		return ret_dict
	
	def sendParameters(self):
		out_dict = self.getFieldsValues()
		out_string = 'p-' + str(out_dict['Nrev']) + '-' + str(out_dict['Pa']) + '-' + str(out_dict['Tas']) + '-' + str(out_dict['Tai'])  + '\n'
		# self.out_label.setText(out_string)
		# print(out_string)
		self.parent().parent().parent().connection_wdg.send2COM(out_string)
		
		response = self.parent().parent().parent().connection_wdg.receiveOnlyCOM()
		if (response == 'ack'):
			self.param_dict = out_dict #update necessary for degree->step conversion (called from angleWidget)
			self.parent().parent().parent().parent().status_bar.showMessage("Parameters set successfully!", STATUS_BAR_TIMEOUT)
			return True
		else:
			raise Exception('Device did not respond')

	def resetParameters(self):
		if self.Nrev_combo.currentText() == self.Nrev_list[5]:
			self.Pa_spinbox.setValue(0)
			self.Tas_spinbox.setValue(0)
			self.Tai_spinbox.setValue(0)
		elif self.Nrev_combo.currentText() == self.Nrev_list[4]:
			self.Pa_spinbox.setValue(0)
			self.Tas_spinbox.setValue(0)
			self.Tai_spinbox.setValue(0)
		elif self.Nrev_combo.currentText() == self.Nrev_list[3]:
			self.Pa_spinbox.setValue(800)
			self.Tas_spinbox.setValue(8)
			self.Tai_spinbox.setValue(0)
		elif self.Nrev_combo.currentText() == self.Nrev_list[2]:
			self.Pa_spinbox.setValue(800)
			self.Tas_spinbox.setValue(16)
			self.Tai_spinbox.setValue(8)
		elif self.Nrev_combo.currentText() == self.Nrev_list[1]:
			self.Pa_spinbox.setValue(800)
			self.Tas_spinbox.setValue(20)
			self.Tai_spinbox.setValue(12)
		elif self.Nrev_combo.currentText() == self.Nrev_list[0]:
			self.Pa_spinbox.setValue(800)
			self.Tas_spinbox.setValue(22)
			self.Tai_spinbox.setValue(14)
		else:
			print('if you see this, there is an error (probably)')
			
	#---------------------------------------------
	def sendMovement(self):
		out_angle = self.angle_spinbox.value()
		out_step = self.angleToStep(out_angle, int(self.param_dict['Nrev']))
		listLetters = ['a', 'l', 'r']
		listRadioBtn = [self.a_radio, self.l_radio, self.r_radio]
		for i in range(len(listRadioBtn)):
			if listRadioBtn[i].isChecked():
				# self.out_label.setText(listLetters[i] + str(out_step))
				self.parent().parent().parent().connection_wdg.send2COM(listLetters[i] + str(out_step))
		
		self.parent().parent().parent().parent().status_bar.showMessage("Moving...", 1000)

		# READ
		received_string = self.parent().parent().parent().connection_wdg.receiveOnlyCOM()
		angle, direction_char, float_list, mean_time, mean_time_total, values_list = self.unpackData(received_string)

		# SAVE CSV
		if self.parent().parent().parent().parent().file_name_flag: # mainWindow
			log_time = time.strftime("%H:%M:%S", time.localtime()) #hh:mm:ss
			log_date = time.strftime("%d %B %Y", time.localtime()) #dd monthName year
			# write into CSV file
			log_text = ''
			for n in range(len(values_list)):
				if n < len(values_list) - 1:
					log_text += values_list[n] + ','
				else:
					log_text += values_list[n]

			dir_string = 'clockwise' if direction_char == 'r' else 'counterclockwise'
			header = 	log_date + ',' + log_time + ',' + \
						mean_time + 'us,' +  mean_time_total + 'us,' + \
						str(int(angle)*360./6400) + 'º,' + dir_string + ',' + \
						str(self.parent().parent().parent().param_wdg.param_dict['Nrev']) + ' step/rev'
			log_text =  header + ',' + log_text + '\n'

			with open(self.parent().parent().parent().parent().file_name,'a') as csvFile:
				csvFile.write(log_text)

		# PLOT
		data_xaxis = self.parent().parent().parent().plot_wdg.updatePlot(float_list, int(angle), direction_char, int(self.param_dict['Nrev']))		

		# COMPUTE DATA STATISTICS (this section MUST be after updatePlot)
		pp, pa = self.computePeakPower(float_list, data_xaxis)
		mp = self.computeMeanPower(float_list)
		rpm = self.computeRPM(int(mean_time_total))

		self.parent().parent().parent().plot_wdg.pp_label.setText(f'PP = {pp:.2f} V')
		self.parent().parent().parent().plot_wdg.pa_label.setText(f'PA = {pa:.2f}º')
		self.parent().parent().parent().plot_wdg.mp_label.setText(f'MP = {mp:.2f} V')
		self.parent().parent().parent().plot_wdg.rpm_label.setText(f'RPM = {rpm:.1f}')

	def sendReset(self):
		self.parent().parent().parent().connection_wdg.send2COM("reset")	
		response = self.parent().parent().parent().connection_wdg.receiveOnlyCOM()
		if (response == 'ack'):			
			self.parent().parent().parent().parent().status_bar.showMessage('Angle reset successfully!', STATUS_BAR_TIMEOUT)
			return True
		else:
			raise Exception('Device did not respond')	

	def angleToStep(self, angle, N_rev):
		step = int(floor(angle * N_rev / 360))
		return step	

	def unpackData(self, received_string):
		values_list = received_string.split('-')[0:-1] # there is an empty char at the end 
		values_list = list(filter(None, values_list)) # delete empty value
		print(values_list) #debug only
		print(len(values_list))
		mean_time = values_list[-5] #microseconds
		mean_time_total = values_list[-4] #microseconds
		angle = values_list[-3]
		direction_char = values_list[-2]
		values_list = values_list[0:-5]  #remove last elements
		float_list = list(map(float,values_list))
		return angle, direction_char, float_list, mean_time, mean_time_total, values_list
		  
	def colorSpin(self, spin, color='#f86e6c'):
		spin.setStyleSheet(f'background-color : {color};')

	def computePeakPower(self, data, data_xaxis):
		if data:
			peak_power = np.max(data)
			peak_angle = data_xaxis[np.argmax(data)]
			return peak_power, peak_angle
		else:
			return 0, 0 

	def computeMeanPower(self, data):
		if data:
			mean_power = np.average(data)
			return mean_power
		else:
			return 0

	def computeRPM(self, mean_step_time):
		if mean_step_time != 0:
			N_max = 6400 	#step/rev, max resolution
			rpm = 10**6 * 60 / (N_max * mean_step_time)
			return rpm
		else:
			return 0

	

if __name__ == '__main__':
	app = QApplication([])
	widget = rightWidget()
	widget.show()
	sys.exit(app.exec_())