import sys
from PySide2.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout, QFormLayout, QVBoxLayout, QRadioButton, QDoubleSpinBox, QSpinBox, QComboBox, QLabel, QButtonGroup
from PySide2.QtCore import QSize, Qt, QThread
from PySide2.QtGui import QIcon, QPixmap
import PySide2.QtCore
from math import floor

import numpy as np

from movementThread import movementThread

# Constants for operation
# -> Angle parameters: degree
LOWEST_DEG = 0 
HIGHEST_DEG = 360*40  # 40 revs
HIGHEST_DEG_ELEV = 360
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
ELEV_RES = 200

class rightWidget(QWidget):
	def __init__(self, central_wdg, main_wdw, parent=None):
		super().__init__(parent)
		self.central_wdg = central_wdg
		self.main_wdw = main_wdw
		#---------------------------------------------
		self.font_dict = {
					"family" : "Segoe UI",
					"title_size" : 14
					}      
		#---------------------------------------------
		# Objects
		self.csv_flag = True
		self.elev_accel_params = {
			'Pa' : 4800,
			'Tas' : 22,
			'Tai' : 12
		}

		#---------------------------------------------
		# Widgets       
		# -> Labels
		self.azimuth_txt = QLabel('<b>Azimuth Settings</b>')
		self.azimuth_txt.setStyleSheet(f"font : {self.font_dict['title_size']}pt '{self.font_dict['family']}';")
		self.azimuth_img = QLabel()
		self.img = QPixmap('img/azimuth.png')
		self.img = self.img.scaled(250, 34, Qt.KeepAspectRatio, Qt.SmoothTransformation)
		self.azimuth_img.setPixmap(self.img)

		self.elevation_txt = QLabel('<b>Elevation Settings</b>')
		self.elevation_txt.setStyleSheet(f"font : {self.font_dict['title_size']}pt '{self.font_dict['family']}';")
		self.elevation_img = QLabel()
		self.img = QPixmap('img/elevation.png')
		self.img = self.img.scaled(250, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
		self.elevation_img.setPixmap(self.img)

		# -> Combo boxes
		self.azimuth_res_combo = QComboBox()
		self.resolution_list = ['1.8 degree/step','0.9 degree/step','0.45 degree/step','0.225 degree/step','0.1125 degree/step','0.05625 degree/step']
		self.azimuth_res_combo.addItems(self.resolution_list)

		self.elevation_res_combo = QComboBox()
		self.elevation_res_combo.addItems(self.resolution_list)

		# -> Spin boxes
		self.Pa_spinbox = QSpinBox()
		self.Tas_spinbox = QSpinBox()
		self.Tai_spinbox = QSpinBox()

		self.angle_azim_spinbox = QDoubleSpinBox()
		self.angle_elev_spinbox = QDoubleSpinBox()

		self.initial_azim_spinbox = QDoubleSpinBox()
		self.final_azim_spinbox = QDoubleSpinBox()
		self.initial_elev_spinbox = QDoubleSpinBox()
		self.final_elev_spinbox = QDoubleSpinBox()


		# -> Radio buttons
		self.a_radio = QRadioButton()
		self.l_radio = QRadioButton()
		self.r_radio = QRadioButton()
		self.azimuth_button_group = QButtonGroup()
		self.azimuth_button_group.addButton(self.a_radio, 0)
		self.azimuth_button_group.addButton(self.l_radio, 1)
		self.azimuth_button_group.addButton(self.r_radio, 2)

		self.a_radio.setIcon(QIcon('img/protractor.png'))
		self.a_radio.setIconSize(QSize(90,60))
		self.a_radio.setFixedSize(90,60)

		self.l_radio.setIcon(QIcon('img/counterclockwise.png'))
		self.l_radio.setIconSize(QSize(90,60))
		self.l_radio.setFixedSize(90,60)

		self.r_radio.setIcon(QIcon('img/clockwise.png'))
		self.r_radio.setIconSize(QSize(90,60))
		self.r_radio.setFixedSize(90,60)


		self.ae_radio = QRadioButton() #
		self.u_radio = QRadioButton()
		self.d_radio = QRadioButton()
		self.elevation_button_group = QButtonGroup()
		self.elevation_button_group.addButton(self.ae_radio, 0)
		self.elevation_button_group.addButton(self.u_radio, 1)
		self.elevation_button_group.addButton(self.d_radio, 2)

		self.ae_radio.setIcon(QIcon('img/protractor.png'))
		self.ae_radio.setIconSize(QSize(90,60))
		self.ae_radio.setFixedSize(90,60)

		self.u_radio.setIcon(QIcon('img/up.png'))
		self.u_radio.setIconSize(QSize(90,60))
		self.u_radio.setFixedSize(90,60)

		self.d_radio.setIcon(QIcon('img/down.png'))
		self.d_radio.setIconSize(QSize(90,60))
		self.d_radio.setFixedSize(90,60)

		# -> Push Buttons
		self.default_btn = QPushButton('Default')
		self.move_azim_btn = QPushButton('Move')
		self.reset_azim_btn = QPushButton('Reset angle')

		self.move_elev_btn = QPushButton('Move') # elevation
		self.reset_elev_btn = QPushButton('Reset angle')

		#---------------------------------------------
		# Init routine 
		self.angleBoxConfig(self.angle_azim_spinbox, LOWEST_DEG, HIGHEST_DEG)
		self.angleBoxConfig(self.angle_elev_spinbox, LOWEST_DEG, HIGHEST_DEG_ELEV)
		self.a_radio.setChecked(True)
		self.ae_radio.setChecked(True)

		self.azimuth_res_combo.setCurrentText(self.resolution_list[5])
		self.elevation_res_combo.setCurrentText(self.resolution_list[0])
		self.NBoxConfig(self.Pa_spinbox)
		self.TimeBoxConfig(self.Tai_spinbox)
		self.TimeBoxConfig(self.Tas_spinbox)

		self.angleBoxConfig(self.initial_azim_spinbox, -180, 180)
		self.angleBoxConfig(self.final_azim_spinbox, -180, 180)

		self.angleBoxConfig(self.initial_elev_spinbox, -30, 60)
		self.angleBoxConfig(self.final_elev_spinbox, -30, 60)

		self.initial_azim_spinbox.setValue(-80)
		self.final_azim_spinbox.setValue(80)
		self.initial_elev_spinbox.setValue(-30)
		self.final_elev_spinbox.setValue(-26)


		#---------------------------------------------
		# Objects
		self.param_dict = self.getFieldsValues()
		self.elev_res = ELEV_RES

		#---------------------------------------------
		# Signals and slots
		self.default_btn.clicked.connect(self.defaultParameters)
		self.connect(self.azimuth_res_combo, PySide2.QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.defaultParameters)

		self.move_azim_btn.clicked.connect(self.sendMovement)
		self.reset_azim_btn.clicked.connect(self.sendReset)

		self.connect(self.elevation_res_combo, PySide2.QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.defaultParametersElev)
		self.move_elev_btn.clicked.connect(self.sendMovementElevation)
		self.reset_elev_btn.clicked.connect(self.sendResetElevation)

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
		param_fields.addRow('Azimuth resolution', self.azimuth_res_combo)
		param_fields.addRow('Acceleration period', self.Pa_spinbox)
		param_fields.addRow('Maximum added delay', self.Tas_spinbox)
		param_fields.addRow('Minimum added delay', self.Tai_spinbox)
		v_layout.addLayout(param_fields)

		# -> Angle SETTINGS
		angle_fields = QFormLayout()
		angle_fields.addRow('Angle', self.angle_azim_spinbox)
		v_layout.addLayout(angle_fields)
		# -> Radio buttons (a, l, r)
		radio_btn_row = QHBoxLayout()
		radio_btn_row.addWidget(self.a_radio)
		radio_btn_row.addWidget(self.l_radio)
		radio_btn_row.addWidget(self.r_radio)
		v_layout.addLayout(radio_btn_row)
		# -> Bottom buttons
		btn_row = QHBoxLayout()
		btn_row.addWidget(self.move_azim_btn)
		btn_row.addWidget(self.reset_azim_btn)
		v_layout.addLayout(btn_row)

		# Routine settings AZIMUTH
		init_final_row = QHBoxLayout()
		init_form = QFormLayout()
		init_form.addRow('Initial angle', self.initial_azim_spinbox)
		init_final_row.addLayout(init_form)
		final_form = QFormLayout()
		final_form.addRow('Final angle', self.final_azim_spinbox)
		init_final_row.addLayout(final_form)
		v_layout.addLayout(init_final_row)

		# -> Title Label ELEVATION
		h_layout = QHBoxLayout()
		h_layout.addWidget(self.elevation_img)
		h_layout.addWidget(self.elevation_txt)
		h_layout.addStretch()
		empty_vspace = QLabel('')
		v_layout.addWidget(empty_vspace)
		v_layout.addLayout(h_layout)

		# -> Elevation resolution
		elev_res_field = QFormLayout()
		elev_res_field.addRow('Elevation resolution', self.elevation_res_combo)
		v_layout.addLayout(elev_res_field)

		# -> ANGLE ELEVATION SETTINGS
		angle_fields = QFormLayout()
		angle_fields.addRow('Angle', self.angle_elev_spinbox)
		v_layout.addLayout(angle_fields)
		# -> Radio buttons (a, l, r)
		radio_btn_row = QHBoxLayout()
		radio_btn_row.addWidget(self.ae_radio)
		radio_btn_row.addWidget(self.u_radio)
		radio_btn_row.addWidget(self.d_radio)
		v_layout.addLayout(radio_btn_row)
		# # -> Bottom buttons
		btn_row = QHBoxLayout()
		btn_row.addWidget(self.move_elev_btn)
		btn_row.addWidget(self.reset_elev_btn)
		v_layout.addLayout(btn_row)
		
		# Routine settings ELEVATION
		init_final_row = QHBoxLayout()
		init_form = QFormLayout()
		init_form.addRow('Initial angle', self.initial_elev_spinbox)
		init_final_row.addLayout(init_form)
		final_form = QFormLayout()
		final_form.addRow('Final angle', self.final_elev_spinbox)
		init_final_row.addLayout(final_form)
		v_layout.addLayout(init_final_row)


		v_layout.addStretch()
		self.setLayout(v_layout)
		self._setToolTips()

	#---------------------------------------------
	def printElevParam(self):
		self.elev_res = int(360/float(self.elevation_res_combo.currentText().split()[0]))
		print(f'Elevation resolution set: {self.elev_res}')

	def getFieldsValues(self):
		ret_dict = {
			'Nrev':int(360/float(self.azimuth_res_combo.currentText().split()[0])),
			'Pa':self.Pa_spinbox.value(),
			'Tas':self.Tas_spinbox.value(),
			'Tai':self.Tai_spinbox.value()
		}
		return ret_dict
	#---------------------------------------------
	def sendMovement(self):
		out_angle = self.angle_azim_spinbox.value()
		out_step = self.angleToStep(out_angle, int(self.param_dict['Nrev']))
		listLetters = ['a', 'l', 'r']
		listRadioBtn = [self.a_radio, self.l_radio, self.r_radio]
		for i in range(len(listRadioBtn)):
			if listRadioBtn[i].isChecked():
				# self.out_label.setText(listLetters[i] + str(out_step))
				self.central_wdg.connection_wdg.send2COM(listLetters[i] + str(out_step))
				print(listLetters[i] + str(out_step))
		
		# Start MOVEMENT
		self.movementRoutine()
	
	def movementRoutine(self):
		# Thread
		self.mov_thread = QThread()
		self.mov_worker = movementThread(self, self.central_wdg, self.main_wdw)
		self.mov_worker.moveToThread(self.mov_thread)
		# Signals
		self.mov_thread.started.connect(self.mov_worker.run)
		self.mov_worker.finished.connect(self.mov_thread.quit)
		self.mov_worker.finished.connect(self.mov_worker.deleteLater)
		self.mov_thread.finished.connect(self.mov_thread.deleteLater)
		self.mov_thread.start()

		# Lock right widget and start, apply buttons
		self.setEnabled(False)
		self.central_wdg.start_btn.setEnabled(False)
		self.central_wdg.apply_btn.setEnabled(False)
		self.central_wdg.connection_wdg.setEnabled(False)

		# Unlock right widget and start, apply buttons
		self.mov_thread.finished.connect(lambda: self.setEnabled(True))
		self.mov_thread.finished.connect(lambda: self.central_wdg.start_btn.setEnabled(True))
		self.mov_thread.finished.connect(lambda: self.central_wdg.apply_btn.setEnabled(True))
		self.mov_thread.finished.connect(lambda: self.central_wdg.connection_wdg.setEnabled(True))

	def sendReset(self):
		self.central_wdg.connection_wdg.send2COM("reset_azim")	
		response = self.central_wdg.connection_wdg.receiveOnlyCOM()
		if (response == 'ack'):			
			self.main_wdw.status_bar.showMessage('Angle reset successfully!', STATUS_BAR_TIMEOUT)
			return True
		else:
			raise Exception('Device did not respond')

	def sendMovementElevation(self):
		out_angle = self.angle_elev_spinbox.value()
		out_step = self.angleToStep(out_angle, self.elev_res)
		listLetters = ['e', 'u', 'd']
		listRadioBtn = [self.ae_radio, self.u_radio, self.d_radio]
		for i in range(len(listRadioBtn)):
			if listRadioBtn[i].isChecked():
				self.central_wdg.connection_wdg.send2COM(listLetters[i] + str(out_step))
				print(listLetters[i] + str(out_step))

	def sendResetElevation(self):
		self.central_wdg.connection_wdg.send2COM("reset_elev")	
		response = self.central_wdg.connection_wdg.receiveOnlyCOM()
		if (response == 'ack'):			
			self.main_wdw.status_bar.showMessage('Angle reset successfully!', STATUS_BAR_TIMEOUT)
			return True
		else:
			raise Exception('Device did not respond')

	def angleToStep(self, angle, N_rev):
		step = int(floor(angle * N_rev / 360))
		return step	

	def unpackData(self, received_string):
		values_list = received_string.split('-')[0:-1] # there is an empty char at the end 
		values_list = list(filter(None, values_list)) # delete empty value
		# print(values_list) #debug only
		# print(len(values_list))
		mean_time = values_list[-5] #microseconds
		mean_time_total = values_list[-4] #microseconds
		angle = values_list[-3]
		direction_char = values_list[-2]
		values_list = values_list[0:-5]  #remove last elements
		float_list = list(map(float,values_list))
		return angle, direction_char, float_list, mean_time, mean_time_total, values_list

	#---------------------------------------------	  
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
	#---------------------------------------------
	def _setToolTips(self):
		self.a_radio.setToolTip('Move to an <b>absolute</b> angle in azimuth')
		self.l_radio.setToolTip('Move <b>counterclockwise</b>')
		self.r_radio.setToolTip('Move <b>clockwise</b>')
		self.move_azim_btn.setToolTip('Rotate <b>azimuth</b> stepper motor')
		self.reset_azim_btn.setToolTip('Set current <b>azimuth</b> position as initial <b>azimuth</b> angle')

		# self.azimuth_res_combo.setToolTip('Angular resolution')
		self.Pa_spinbox.setToolTip('Number of steps <b>between \nminimum</b> added delay and <b>\nmaximum</b> added delay')
		self.Tas_spinbox.setToolTip('<b>Maximum delay</b> added to <b>each step</b> \n to decrease rotation speed')
		self.Tai_spinbox.setToolTip('<b>Minimum delay</b> added to <b>each step</b> \n to decrease rotation speed')
		self.default_btn.setToolTip('Set optimum empirical parameters to <b>maximise</b> rotation speed while keeping a <b>stable behaviour</b> of stepper motor')

		self.ae_radio.setToolTip('Move to an <b>absolute</b> angle in elevation')
		self.u_radio.setToolTip('Move <b>upwards</b>')
		self.d_radio.setToolTip('Move <b>downwards</b>')
		self.move_elev_btn.setToolTip('Rotate <b>elevation</b> stepper motor')
		self.reset_elev_btn.setToolTip('Set current <b>elevation</b> position as initial <b>elevation</b> angle')

		self.central_wdg.apply_btn.setToolTip('<b>Send command</b> to set parameters')
		self.central_wdg.start_btn.setToolTip('Start <b>routine</b>')

		self.initial_azim_spinbox.setToolTip('<b>Routine: </b>Set <b>initial</b> azimuth angle')
		self.final_azim_spinbox.setToolTip('<b>Routine: </b>Set <b>final</b> azimuth angle')
		self.initial_elev_spinbox.setToolTip('<b>Routine: </b>Set <b>initial</b> elevation angle')
		self.final_elev_spinbox.setToolTip('<b>Routine: </b>Set <b>final</b> elevation angle')

		self.angle_azim_spinbox.setToolTip('Set a <b>movement</b> azimuth angle')
		self.angle_elev_spinbox.setToolTip('Set a <b>movement</b> elevation angle')
	#---------------------------------------------
	def angleBoxConfig(self, box, lowest_deg, highest_deg):
		box.setMinimum(lowest_deg)
		box.setMaximum(highest_deg)
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

	def defaultParameters(self):
		local_Pa = 4800
		if self.azimuth_res_combo.currentText() == self.resolution_list[5]:
			self.Pa_spinbox.setValue(local_Pa)
			self.Tas_spinbox.setValue(10)
			self.Tai_spinbox.setValue(2)
		elif self.azimuth_res_combo.currentText() == self.resolution_list[4]:
			self.Pa_spinbox.setValue(local_Pa)
			self.Tas_spinbox.setValue(20)
			self.Tai_spinbox.setValue(4)
		elif self.azimuth_res_combo.currentText() == self.resolution_list[3]:
			self.Pa_spinbox.setValue(local_Pa)
			self.Tas_spinbox.setValue(40)
			self.Tai_spinbox.setValue(8)
		elif self.azimuth_res_combo.currentText() == self.resolution_list[2]:
			self.Pa_spinbox.setValue(local_Pa)
			self.Tas_spinbox.setValue(40)
			self.Tai_spinbox.setValue(8)
		elif self.azimuth_res_combo.currentText() == self.resolution_list[1]:
			self.Pa_spinbox.setValue(local_Pa)
			self.Tas_spinbox.setValue(40)
			self.Tai_spinbox.setValue(8)
		elif self.azimuth_res_combo.currentText() == self.resolution_list[0]:
			self.Pa_spinbox.setValue(local_Pa)
			self.Tas_spinbox.setValue(40)
			self.Tai_spinbox.setValue(8)
		else:
			print('if you see this, there is an error (probably)')

	def defaultParametersElev(self):
		self.elev_res = int(360/float(self.elevation_res_combo.currentText().split()[0]))
		local_Pa = 4800
		if self.elevation_res_combo.currentText() == self.resolution_list[5]:
			self.elev_accel_params['Pa'] = local_Pa
			self.elev_accel_params['Tas'] = 10
			self.elev_accel_params['Tai'] = 2
		elif self.elevation_res_combo.currentText() == self.resolution_list[4]:
			self.elev_accel_params['Pa'] = local_Pa
			self.elev_accel_params['Tas'] = 20
			self.elev_accel_params['Tai'] = 4
		elif self.elevation_res_combo.currentText() == self.resolution_list[3]:
			self.elev_accel_params['Pa'] = local_Pa
			self.elev_accel_params['Tas'] = 40
			self.elev_accel_params['Tai'] = 8
		elif self.elevation_res_combo.currentText() == self.resolution_list[2]:
			self.elev_accel_params['Pa'] = local_Pa
			self.elev_accel_params['Tas'] = 40
			self.elev_accel_params['Tai'] = 8
		elif self.elevation_res_combo.currentText() == self.resolution_list[1]:
			self.elev_accel_params['Pa'] = local_Pa
			self.elev_accel_params['Tas'] = 40
			self.elev_accel_params['Tai'] = 8
		elif self.elevation_res_combo.currentText() == self.resolution_list[0]:
			self.elev_accel_params['Pa'] = local_Pa
			self.elev_accel_params['Tas'] = 40
			self.elev_accel_params['Tai'] = 8
		else:
			print('if you see this, there is an error (probably) ELEVATION')
	

if __name__ == '__main__':
	app = QApplication([])
	widget = rightWidget()
	widget.show()
	sys.exit(app.exec_())