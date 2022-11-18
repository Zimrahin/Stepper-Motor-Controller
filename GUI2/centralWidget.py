import sys 
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame, QPushButton
from PySide2 import QtGui
from PySide2.QtCore import Qt, QThread
from PySide2.QtGui import QPalette, QColor, QPixmap, QFont

from connectionWidget import connectionWidget
from rightWidget import rightWidget
from plotWidget import plotWidget
from workerThread import workerThreadPlotUpdate

import time

# https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
import ctypes
myappid = 'StepperMotorController' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

STATUS_BAR_TIMEOUT = 5000

class centralWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowIcon(QtGui.QIcon('img/logo.png'))
		self.setWindowTitle("Stepper motor controller")

		#Objects 
		self.COM = None
		# ------------------------------------------------------------
		# Widgets

		self.apply_btn = QPushButton('Apply')
		self.start_btn = QPushButton('Start')
		self.start_btn.setStyleSheet("background-color : '#054d45';")

		# -> Serial Connection Widget
		self.connection_wdg = connectionWidget(self)

		# -> Plot Widget
		self.plot_wdg = plotWidget(self)

		# -> Logo Widget
		self.logo_wdg = logoWidget(self)

		# -> Right Scroll Widget
		self.right_wdg = rightWidget(self)
		
		# ->-> Scroll Area
		self.scroll_area = QScrollArea()

		# self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.scroll_area.setWidgetResizable(True)
		self.scroll_area.setFrameShape(QFrame.NoFrame)
		self.scroll_area.setMinimumWidth(360)
		self.scroll_area.setWidget(self.right_wdg)

		# ------------------------------------------------------------
		# Init routines
		self.right_wdg.setEnabled(False)
		self.start_btn.setEnabled(False)
		self.apply_btn.setEnabled(False)

		# Signals and Slots
		self.connection_wdg.connect_signal.connect(self.connectUnlock)
		self.connection_wdg.disconnect_signal.connect(self.disconnectLock)

		self.apply_btn.clicked.connect(self.applyParameters)
		self.start_btn.clicked.connect(self.startRoutine)
		# ------------------------------------------------------------
		# Layout
		v_layout = QVBoxLayout()
		
		v_layout.addWidget(self.connection_wdg)
		# v_layout.addWidget(self.right_wdg)
		v_layout.addWidget(self.scroll_area)
		# v_layout.addStretch()
		v_layout.addWidget(self.apply_btn)
		v_layout.addWidget(self.start_btn)

		v_layout.addWidget(self.logo_wdg)
		

		h_layout = QHBoxLayout()
		h_layout.addWidget(self.plot_wdg, 6)
		h_layout.addLayout(v_layout, 1)

		self.setLayout(h_layout)

	def applyParameters(self):
		out_dict = self.right_wdg.getFieldsValues()
		out_string = 'p-' + str(out_dict['Nrev']) + '-' + str(out_dict['Pa']) + '-' + str(out_dict['Tas']) + '-' + str(out_dict['Tai']) + '-' + str(self.right_wdg.elev_res) + '\n'
		print(out_string)
		self.connection_wdg.send2COM(out_string)
		
		response = self.connection_wdg.receiveOnlyCOM()
		if (response == 'ack'):
			self.right_wdg.param_dict = out_dict #update necessary for degree->step conversion (called from angleWidget)
			self.parent().status_bar.showMessage("Parameters set successfully!", STATUS_BAR_TIMEOUT)
			return True
		else:
			raise Exception('Device did not respond')

	def startRoutine(self):
		# initial and final angles from spinboxes
		azim_init_angle = self.right_wdg.initial_azim_spinbox.value()
		azim_final_angle = self.right_wdg.final_azim_spinbox.value()
		elev_init_angle = self.right_wdg.initial_elev_spinbox.value()
		elev_final_angle = self.right_wdg.final_elev_spinbox.value()

		# initial and final steps to be sent to Arduino
		azim_init_step = self.right_wdg.angleToStep(azim_init_angle, int(self.right_wdg.param_dict['Nrev']))
		azim_final_step = self.right_wdg.angleToStep(azim_final_angle, int(self.right_wdg.param_dict['Nrev']))
		elev_init_step = self.right_wdg.angleToStep(elev_init_angle, self.right_wdg.elev_res)
		elev_final_step = self.right_wdg.angleToStep(elev_final_angle, self.right_wdg.elev_res)

		out_string = f'n-a{azim_init_step}-a{azim_final_step}-e{elev_init_step}-e{elev_final_step}'

		print(out_string)
		self.connection_wdg.send2COM(out_string)
		# Start LOOOOOOONG routine 
		self.longUpdatePlotRoutine()

	def disconnectLock(self):
		self.COM = None
		self.right_wdg.setEnabled(False)
		self.start_btn.setEnabled(False)
		self.apply_btn.setEnabled(False)

	def connectUnlock(self):
		self.COM = self.connection_wdg.serial_COM
		self.right_wdg.setEnabled(True)
		self.start_btn.setEnabled(True)
		self.apply_btn.setEnabled(True)

	def longUpdatePlotRoutine(self):
		# Create QThread object
		self.thread = QThread()
		# Create a worker object
		self.worker = workerThreadPlotUpdate(self.connection_wdg, self.plot_wdg, self.right_wdg)
		# Move worker to the thread
		self.worker.moveToThread(self.thread)
		# Connect signals and slots
		self.thread.started.connect(self.worker.run)
		self.worker.finished.connect(self.thread.quit)
		self.worker.finished.connect(self.worker.deleteLater)
		self.thread.finished.connect(self.thread.deleteLater)
		# self.worker.progress.connect(self.reportProgress) # useful por a progress bar
		# Start the thread
		self.thread.start()


		# Lock right widget and start, apply buttons
		self.right_wdg.setEnabled(False)
		self.start_btn.setEnabled(False)
		self.apply_btn.setEnabled(False)
		self.connection_wdg.setEnabled(False)

		# Unlock right widget and start, apply buttons
		self.thread.finished.connect(lambda: self.right_wdg.setEnabled(True))
		self.thread.finished.connect(lambda: self.start_btn.setEnabled(True))
		self.thread.finished.connect(lambda: self.apply_btn.setEnabled(True))
		self.thread.finished.connect(lambda: self.connection_wdg.setEnabled(True))



class logoWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.logo_wdg = QLabel()
		self.img = QPixmap('img/logo2.png')
		self.img = self.img.scaled(250, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
		self.logo_wdg.setPixmap(self.img)
		# self.setMaximumHeight(100)
		# self.setMaximumWidth(354)

		# Layout
		layout = QHBoxLayout()
		layout.addStretch()
		layout.addWidget(self.logo_wdg)
		
		self.setLayout(layout)



def darkMode():
	# Dark Theme
	# Adapted from https://github.com/pyqt/examples/tree/_/src/09%20Qt%20dark%20theme
	palette = QPalette()
	palette.setColor(QPalette.Window, QColor(53, 53, 53))
	palette.setColor(QPalette.WindowText, Qt.white)
	palette.setColor(QPalette.Base, QColor(25, 25, 25))
	palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
	palette.setColor(QPalette.ToolTipBase, Qt.black)
	palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
	palette.setColor(QPalette.Text, Qt.white)
	palette.setColor(QPalette.Button, QColor(53, 53, 53))
	palette.setColor(QPalette.ButtonText, Qt.white)
	palette.setColor(QPalette.BrightText, Qt.red)
	palette.setColor(QPalette.Link, QColor(42, 130, 218))
	palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
	palette.setColor(QPalette.HighlightedText, Qt.black)
	palette.setColor(QPalette.Disabled, QPalette.Base, QColor(49, 49, 49))
	palette.setColor(QPalette.Disabled, QPalette.Text, QColor(90, 90, 90))
	palette.setColor(QPalette.Disabled, QPalette.Button, QColor(42, 42, 42))
	palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(90, 90, 90))
	palette.setColor(QPalette.Disabled, QPalette.Window, QColor(49, 49, 49))
	palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(90, 90, 90))
	return palette


if __name__ == '__main__':
	app = QApplication([])
	# if os.name == 'nt': # New Technology GUI (Windows)
	app.setStyle('fusion') 
	palette = darkMode()
	app.setPalette(palette)
	app.setFont(QFont("Arial", 9))
		
	widget = centralWidget()
	widget.show()

	sys.exit(app.exec_())