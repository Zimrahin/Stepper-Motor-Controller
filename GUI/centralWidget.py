import sys 
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame, QPushButton
from PySide2 import QtGui
from PySide2.QtCore import Qt, QThread
from PySide2.QtGui import QPixmap

from connectionWidget import connectionWidget
from rightWidget import rightWidget
from plotWidget import plotWidget
from routineThread import workerThreadPlotUpdate

import time
from messageBox import errorBox

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
		self.start_btn.setStyleSheet("QPushButton{background-color : '#054d45';}")

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
		self.scroll_area.setMinimumWidth(370) 
		self.scroll_area.setWidget(self.right_wdg)

		# ------------------------------------------------------------
		# Init routines
		self.right_wdg.setEnabled(False)
		self.start_btn.setEnabled(False)
		self.apply_btn.setEnabled(False)

		# Signals and Slots
		self.connection_wdg.connect_signal.connect(lambda: self.connectUnlock(True))
		self.connection_wdg.disconnect_signal.connect(lambda: self.connectUnlock(False))

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
		h_layout.addWidget(self.plot_wdg, 5)
		h_layout.addLayout(v_layout, 1)

		self.setLayout(h_layout)

	def applyParameters(self):
		Pa_elev = str(self.right_wdg.elev_accel_params['Pa'])
		Tas_elev = str(self.right_wdg.elev_accel_params['Tas'])
		Tai_elev = str(self.right_wdg.elev_accel_params['Tai'])
		out_dict = self.right_wdg.getFieldsValues()
		out_string = 'p-' + str(out_dict['Nrev']) + '-' + str(out_dict['Pa']) + '-' + str(out_dict['Tas']) + '-' + str(out_dict['Tai']) + '-' + str(self.right_wdg.elev_res) + '-' + Pa_elev + '-' + Tas_elev + '-' + Tai_elev + '\n'
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
		azim_diff_angle = azim_final_angle - azim_init_angle

		elev_init_angle = self.right_wdg.initial_elev_spinbox.value()
		elev_final_angle = self.right_wdg.final_elev_spinbox.value()
		
		if azim_init_angle < 0:
			azim_init_angle += 360
		if azim_final_angle < 0:
			azim_final_angle += 360
		if elev_init_angle < 0:
			elev_init_angle += 360
		if elev_final_angle < 0:
			elev_final_angle += 360

		dir_char = 'l' if azim_diff_angle > 0 else 'r'
		azim_diff_angle = abs(azim_diff_angle)

		# initial and final steps to be sent to Arduino
		azim_init_step = self.right_wdg.angleToStep(azim_init_angle, int(self.right_wdg.param_dict['Nrev']))
		azim_diff_step = self.right_wdg.angleToStep(azim_diff_angle, int(self.right_wdg.param_dict['Nrev']))

		elev_init_step = self.right_wdg.angleToStep(elev_init_angle, self.right_wdg.elev_res)
		elev_final_step = self.right_wdg.angleToStep(elev_final_angle, self.right_wdg.elev_res)

		out_string = f'n-a{azim_init_step}-{dir_char}{azim_diff_step}-e{elev_init_step}-e{elev_final_step}'

		print(out_string)
		self.connection_wdg.send2COM(out_string)

		# Start LOOOOOOONG routine 
		self.longUpdatePlotRoutine()

	def longUpdatePlotRoutine(self):
		# Create QThread object
		self.routine_thread = QThread()
		# Create a worker object
		self.routine_worker = workerThreadPlotUpdate(self.connection_wdg, self.plot_wdg, self.right_wdg)
		# Move worker to the thread
		self.routine_worker.moveToThread(self.routine_thread)
		# Connect signals and slots
		self.routine_thread.started.connect(self.routine_worker.run)
		self.routine_worker.finished.connect(self.routine_thread.quit)
		self.routine_worker.finished.connect(self.routine_worker.deleteLater)
		self.routine_thread.finished.connect(self.routine_thread.deleteLater)
		# self.worker.progress.connect(self.reportProgress) # useful por a progress bar
		# Start the thread
		self.routine_thread.start()

		# Lock right widget and start, apply buttons
		self.right_wdg.setEnabled(False)
		self.start_btn.setEnabled(False)
		self.apply_btn.setEnabled(False)
		self.connection_wdg.setEnabled(False)

		# Unlock right widget and start, apply buttons
		self.routine_thread.finished.connect(lambda: self.right_wdg.setEnabled(True))
		self.routine_thread.finished.connect(lambda: self.start_btn.setEnabled(True))
		self.routine_thread.finished.connect(lambda: self.apply_btn.setEnabled(True))
		self.routine_thread.finished.connect(lambda: self.connection_wdg.setEnabled(True))

	def connectUnlock(self, flag: bool):
		self.COM = self.connection_wdg.serial_COM if flag else None
		self.right_wdg.setEnabled(flag)
		self.start_btn.setEnabled(flag)
		self.apply_btn.setEnabled(flag)


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


if __name__ == '__main__':
	app = QApplication([])
	# if os.name == 'nt': # New Technology GUI (Windows)
	app.setStyle('fusion') 

	widget = centralWidget()
	widget.show()

	sys.exit(app.exec_())