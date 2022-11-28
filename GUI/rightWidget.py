__author__ = 'github.com/Zimrahin'

import sys
from PySide2.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout, QFormLayout, QVBoxLayout, QRadioButton, QDoubleSpinBox, QSpinBox, QComboBox, QLabel, QButtonGroup
from PySide2.QtCore import QSize, Qt, QThread
from PySide2.QtGui import QIcon, QPixmap
import PySide2.QtCore
from math import floor

import numpy as np
import struct

from movementThread import movementThread

class rightWidget(QWidget):
	def __init__(self, central_wdg, main_wdw, parent=None):
		super().__init__(parent)
		self.central_wdg = central_wdg
		self.main_wdw = main_wdw
		self.config = main_wdw.config     

		#---------------------------------------------------------
		# Widgets       
		# -> Labels
		self.azimuth_txt = QLabel('<b>Azimuth Settings</b>')
		self.azimuth_txt.setStyleSheet(f"font : {self.config.dict['font']['mega_title_size']}pt '{self.config.dict['font']['family']}';")
		self.azimuth_img = QLabel()
		self.img = QPixmap('img/azimuth.png')
		self.img = self.img.scaled(250, 34, Qt.KeepAspectRatio, Qt.SmoothTransformation)
		self.azimuth_img.setPixmap(self.img)

		self.elevation_txt = QLabel('<b>Elevation Settings</b>')
		self.elevation_txt.setStyleSheet(f"font : {self.config.dict['font']['mega_title_size']}pt '{self.config.dict['font']['family']}';")
		self.elevation_img = QLabel()
		self.img = QPixmap('img/elevation.png')
		self.img = self.img.scaled(250, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
		self.elevation_img.setPixmap(self.img)

		# -> Combo boxes
		self.resolutions = self.config.dict['resolutions']['list']
		units = self.config.dict['resolutions']['units']
		self.resolution_list = [f'{a}{units}' for a in self.resolutions]

		self.azimuth_res_combo = QComboBox()
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


		self.e_radio = QRadioButton() 
		self.u_radio = QRadioButton()
		self.d_radio = QRadioButton()
		self.elevation_button_group = QButtonGroup()
		self.elevation_button_group.addButton(self.e_radio, 0)
		self.elevation_button_group.addButton(self.u_radio, 1)
		self.elevation_button_group.addButton(self.d_radio, 2)

		self.e_radio.setIcon(QIcon('img/protractor.png'))
		self.e_radio.setIconSize(QSize(90,60))
		self.e_radio.setFixedSize(90,60)

		self.u_radio.setIcon(QIcon('img/up.png'))
		self.u_radio.setIconSize(QSize(90,60))
		self.u_radio.setFixedSize(90,60)

		self.d_radio.setIcon(QIcon('img/down.png'))
		self.d_radio.setIconSize(QSize(90,60))
		self.d_radio.setFixedSize(90,60)

		# -> Push Buttons
		self.move_azim_btn = QPushButton('Move')
		self.reset_azim_btn = QPushButton('Reset angle')

		self.move_elev_btn = QPushButton('Move')
		self.reset_elev_btn = QPushButton('Reset angle')

		#---------------------------------------------------------
		# Init routine 
		self.a_radio.setChecked(True)
		self.e_radio.setChecked(True)
		
		self.azimuth_res_combo.setCurrentText(self.resolution_list[self.config.dict['resolutions']['default_azim']])
		self.elevation_res_combo.setCurrentText(self.resolution_list[self.config.dict['resolutions']['default_elev']])
		
		# Set step increment, lowest and highest values, units of spin boxes
		self._wrapBoxConfig()
		
		self.defaultParametersAzim()
		self.azim_params = self.getFieldsValues()
		self.elev_params = {}
		self.defaultParametersElev()

		#---------------------------------------------------------
		# Signals and slots
		self.connect(self.azimuth_res_combo, PySide2.QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.defaultParametersAzim)

		self.move_azim_btn.clicked.connect(self.sendMovementAzimuth)
		self.reset_azim_btn.clicked.connect(lambda: self.sendReset('Azimuth'))

		self.connect(self.elevation_res_combo, PySide2.QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.defaultParametersElev)
		self.move_elev_btn.clicked.connect(self.sendMovementElevation)
		self.reset_elev_btn.clicked.connect(lambda: self.sendReset('Elevation'))

		#---------------------------------------------------------
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
		# -> Radio buttons (e, u, d)
		radio_btn_row = QHBoxLayout()
		radio_btn_row.addWidget(self.e_radio)
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
		
	#-----------------------------------------------------------------------
	def sendMovementAzimuth(self):
		out_angle = self.angle_azim_spinbox.value()
		out_step = self.angleToStep(out_angle, int(self.azim_params['Nrev']))
		listLetters = ['a', 'l', 'r']
		listRadioBtn = [self.a_radio, self.l_radio, self.r_radio]
		for i in range(len(listRadioBtn)):
			if listRadioBtn[i].isChecked():
				self.central_wdg.connection_wdg.send2COM(listLetters[i] + str(out_step))
				if self.config.dict['debug_print']:
					print(listLetters[i] + str(out_step))
		
		# Start MOVEMENT thread
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
		
	#-----------------------------------------------------------------------
	def sendMovementElevation(self):
		out_angle = self.angle_elev_spinbox.value()
		out_step = self.angleToStep(out_angle, self.elev_params['Nrev'])
		listLetters = ['e', 'u', 'd']
		listRadioBtn = [self.e_radio, self.u_radio, self.d_radio]
		for i in range(len(listRadioBtn)):
			if listRadioBtn[i].isChecked():
				self.central_wdg.connection_wdg.send2COM(listLetters[i] + str(out_step))
				if self.config.dict['debug_print']:
					print(listLetters[i] + str(out_step))

	#-----------------------------------------------------------------------
	def sendReset(self, motor : str):
		if motor == 'Azimuth':
			reset_str = 'reset_azim'
		if motor == 'Elevation':
			reset_str = 'reset_elev'
		self.central_wdg.connection_wdg.send2COM(reset_str)	
		response = self.central_wdg.connection_wdg.receiveOnlyCOM()
		if (response == 'ack'):			
			self.main_wdw.status_bar.showMessage(f'{motor} angle reset successfully!', self.config.dict['status_bar_timeout'])
			return True
		else:
			raise Exception('Device did not respond')

	#-----------------------------------------------------------------------
	def angleToStep(self, angle, N_rev):
		step = int(floor(angle * N_rev / 360))
		return step	

	#-----------------------------------------------------------------------
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

	def unpackDataBytes(self, data):
		size_of_int = 4
		size_of_char = 1
		size_of_float = 4

		# compute amount of int data
		n_int = 4
		n_int_str = 'i'*n_int #'iiii'

		# compute amount of char data
		n_char = 2
		n_char_str = 'c'*n_char #'cc'

		# compute amount of float data
		n_float = int(len(data) - n_int*size_of_int - n_char*size_of_char) # extract metadata. Last char is \n
		n_float = int(n_float/size_of_float)
		n_float_str = 'f'*n_float

		values_tuple = struct.unpack(n_float_str + n_int_str + n_char_str, data) #returns tuple

		mean_time = values_tuple[-6] #microseconds
		mean_time_total = values_tuple[-5] #microseconds
		angle = values_tuple[-4]
		steps_to_move = values_tuple[-3]
		direction_char = values_tuple[-2]
		float_tuple = values_tuple[0:-6]  #remove last elements
		float_list = list(float_tuple)

		return angle, direction_char, float_list, mean_time, mean_time_total

	#-----------------------------------------------------------------------	 
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

	#-----------------------------------------------------------------------
	def _setToolTips(self):
		self.a_radio.setToolTip('Move to an <b>absolute</b> angle in azimuth')
		self.l_radio.setToolTip('Move <b>counterclockwise</b>')
		self.r_radio.setToolTip('Move <b>clockwise</b>')
		self.move_azim_btn.setToolTip('Rotate <b>azimuth</b> stepper motor')
		self.reset_azim_btn.setToolTip('Set current <b>azimuth</b> position as initial <b>azimuth</b> angle')

		self.Pa_spinbox.setToolTip('Number of steps <b>between \nminimum</b> added delay and <b>\nmaximum</b> added delay')
		self.Tas_spinbox.setToolTip('<b>Maximum delay</b> added to <b>each step</b> \n to decrease rotation speed')
		self.Tai_spinbox.setToolTip('<b>Minimum delay</b> added to <b>each step</b> \n to decrease rotation speed')

		self.e_radio.setToolTip('Move to an <b>absolute</b> angle in elevation')
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
	#-----------------------------------------------------------------------
	def _spinBoxConfig(self, box, lowest, highest, step, units):
		box.setMinimum(lowest)
		box.setMaximum(highest)
		box.setSingleStep(step)
		box.setSuffix(units)

	#-----------------------------------------------------------------------
	def getFieldsValues(self):
		ret_dict = {
			'Nrev':int(360/float(self.azimuth_res_combo.currentText().split()[0])),
			'Pa':self.Pa_spinbox.value(),
			'Tas':self.Tas_spinbox.value(),
			'Tai':self.Tai_spinbox.value()
		}
		return ret_dict

	#-----------------------------------------------------------------------
	def defaultParametersAzim(self):
		local_Pa = self.config.dict['default_params']['Pa']
		for i in range(len(self.resolution_list)):
			if self.azimuth_res_combo.currentText() == self.resolution_list[i]:
				local_Tas = self.config.dict['default_params']['delays'][i]['Tas']
				local_Tai = self.config.dict['default_params']['delays'][i]['Tai']

				self.Pa_spinbox.setValue(local_Pa)
				self.Tas_spinbox.setValue(local_Tas)
				self.Tai_spinbox.setValue(local_Tai)
				return
		print('Error in defaultParametersAzim()')

	def defaultParametersElev(self):
		self.elev_params['Nrev'] = int(360/float(self.elevation_res_combo.currentText().split()[0]))
		local_Pa = self.config.dict['default_params']['Pa']
		for i in range(len(self.resolution_list)):
			if self.azimuth_res_combo.currentText() == self.resolution_list[i]:
				local_Tas = self.config.dict['default_params']['delays'][i]['Tas']
				local_Tai = self.config.dict['default_params']['delays'][i]['Tai']

				self.elev_params['Pa'] = local_Pa
				self.elev_params['Tas'] = local_Tas
				self.elev_params['Tai'] = local_Tai
				return
		print('Error in defaultParametersElev()')
	#-----------------------------------------------------------------------
	def _wrapBoxConfig(self):
		self._spinBoxConfig(self.angle_azim_spinbox, self.config.dict['azim_angle_spin']['lowest'], self.config.dict['azim_angle_spin']['highest'], self.config.dict['azim_angle_spin']['step'], self.config.dict['azim_angle_spin']['units'])

		self._spinBoxConfig(self.angle_elev_spinbox, self.config.dict['elev_angle_spin']['lowest'], self.config.dict['elev_angle_spin']['highest'], self.config.dict['elev_angle_spin']['step'], self.config.dict['elev_angle_spin']['units'])
		
		self._spinBoxConfig(self.Pa_spinbox, self.config.dict['Pa_spin']['lowest'], self.config.dict['Pa_spin']['highest'], self.config.dict['Pa_spin']['step'], self.config.dict['Pa_spin']['units'])

		self._spinBoxConfig(self.Tai_spinbox, self.config.dict['delay_spin']['lowest'], self.config.dict['delay_spin']['highest'], self.config.dict['delay_spin']['step'], self.config.dict['delay_spin']['units'])

		self._spinBoxConfig(self.Tas_spinbox, self.config.dict['delay_spin']['lowest'], self.config.dict['delay_spin']['highest'], self.config.dict['delay_spin']['step'], self.config.dict['delay_spin']['units'])

		self._spinBoxConfig(self.initial_azim_spinbox, self.config.dict['azim_angle_spin']['routine']['lowest'], self.config.dict['azim_angle_spin']['routine']['highest'], self.config.dict['azim_angle_spin']['step'], self.config.dict['azim_angle_spin']['units'])

		self._spinBoxConfig(self.final_azim_spinbox, self.config.dict['azim_angle_spin']['routine']['lowest'], self.config.dict['azim_angle_spin']['routine']['highest'], self.config.dict['azim_angle_spin']['step'], self.config.dict['azim_angle_spin']['units'])

		self._spinBoxConfig(self.initial_elev_spinbox, self.config.dict['elev_angle_spin']['routine']['lowest'], self.config.dict['elev_angle_spin']['routine']['highest'], self.config.dict['elev_angle_spin']['step'], self.config.dict['elev_angle_spin']['units'])

		self._spinBoxConfig(self.final_elev_spinbox, self.config.dict['elev_angle_spin']['routine']['lowest'], self.config.dict['elev_angle_spin']['routine']['highest'], self.config.dict['elev_angle_spin']['step'], self.config.dict['elev_angle_spin']['units'])

		self.initial_azim_spinbox.setValue(self.config.dict['azim_angle_spin']['routine']['default_i'])
		self.final_azim_spinbox.setValue(self.config.dict['azim_angle_spin']['routine']['default_f'])
		self.initial_elev_spinbox.setValue(self.config.dict['elev_angle_spin']['routine']['default_i'])
		self.final_elev_spinbox.setValue(self.config.dict['elev_angle_spin']['routine']['default_f'])

if __name__ == '__main__':
	app = QApplication([])
	widget = rightWidget()
	widget.show()
	sys.exit(app.exec_())