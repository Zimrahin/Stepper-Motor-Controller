__author__ = 'github.com/Zimrahin'

import sys
import time
from PySide2 import QtGui
from PySide2.QtCore import Qt, QUrl
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QMenuBar, QMenu, QAction, QFileDialog, QMessageBox
from PySide2.QtGui import QDesktopServices

from centralWidget import centralWidget
from darkPalette import darkPalette
from JSONhandler import JSONreader, JSONwriter

class mainWindow(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.config = JSONreader('config.json')
		self._palette = JSONreader('palette.json').dict
		self.setWindowTitle(self.config.dict['app_name'])
		self.setWindowIcon(QtGui.QIcon('img/logo.png'))
		self._setStyleSheet()
		self.move(self.config.dict['startup_location'][0],self.config.dict['startup_location'][1])

		#Objects
		self.file_name_flag = False
		self.file_name = ''

		# Widgets
		# -> Central Widget
		self.central_wdg = centralWidget(self, self)
		self.setCentralWidget(self.central_wdg)

		# Status Bar
		self.status_bar = self.statusBar()
		self.permanent_message = QLabel(f"Version {self.config.dict['version']}")
		self.permanent_message.setStyleSheet('color : ' + self._palette['version_label'])
		self.permanent_message.setAlignment(Qt.AlignRight)
		self.status_bar.addPermanentWidget(self.permanent_message)

		self._createActions()
		self._createMenuBar()
		self._connectActions()

	# Creates Menu Bar (at the top, below the title bar)
	def _createMenuBar(self):
		menu_bar = QMenuBar(self)
		self.setMenuBar(menu_bar)

		file_menu = QMenu("File", self)
		help_menu = QMenu("Help", self)
		menu_bar.addMenu(file_menu)
		menu_bar.addMenu(help_menu)

		#Actions
		file_menu.addAction(self.save_settings)
		file_menu.addAction(self.open_settings)
		file_menu.addSeparator()
		file_menu.addAction(self.save_action)
		file_menu.addAction(self.open_action)
		file_menu.addSeparator()
		file_menu.addAction(self.exit_action)

		help_menu.addAction(self.help_contentAction)
		help_menu.addSeparator()
		help_menu.addAction(self.about_action)

	# Creates Menu Bar actions
	def _createActions(self):
		self.save_settings = QAction("Save Routine Settings", self)
		self.open_settings = QAction('Open Routine Settings', self)
		self.save_action = QAction("New Save File", self)
		self.open_action = QAction('Open CSV data', self)
		self.exit_action = QAction("Exit", self)

		self.help_contentAction = QAction("Help Content", self)
		self.about_action = QAction("About", self)

	# This method is called to create a file to start storing acquired data.
	# File is initialised with a header.
	def saveFile(self):
		options = QFileDialog.Options()
		# options |= QFileDialog.DontUseNativeDialog
		file_name, _ = QFileDialog.getSaveFileName(self,'New Save File',time.strftime("csv_files/%d_%B_%Y_%Hh_%Mm_%Ss.csv", time.localtime()),"All Files (*);;CSV (Comma delimited) (*.csv)", options=options)
		if file_name:
			if file_name[-4:] != '.csv':
				file_name += '.csv'
			self.status_bar.showMessage(f'Selected path: {file_name}', self.config.dict['status_bar_timeout'])
			# Only for CSV writing afterwards
			self.file_name_flag = True
			self.file_name = file_name

			header = 'Date,Time,RPM,Last azimuth angle (°),Movement direction,Azimuth resolution (steps/rev),Current elevation angle (°),Repetition number,Elevation resolution (steps/rev),Data\n'
			with open(self.file_name,'w') as csvFile:
				csvFile.write(header)
	
	# When a CSV file is created, this method is called to save measured data.
	def saveCSV(self, file_name, float_list, rpm, azim_step, direction_char, azim_res, elev_step, n_repetition, elev_res):
		log_time = time.strftime("%H:%M:%S", time.localtime()) #hh:mm:ss
		log_date = time.strftime("%d %B %Y", time.localtime()) #dd monthName year

		log_text = ''
		for n in range(len(float_list)):
			if n < len(float_list) - 1:
				log_text += str(float_list[n]) + ','
			else:
				log_text += str(float_list[n])
						
		dir_string = 'clockwise' if direction_char == 'r' else 'counterclockwise'
								
		header_left = 	f'{log_date},{log_time},{rpm:.2f},{int(azim_step)*360./6400},{dir_string},{azim_res},{int(elev_step)*360./6400},{n_repetition},{elev_res}'
		
		log_text = f'{header_left},{log_text}\n'

		with open(file_name,'a') as csvFile:
			csvFile.write(log_text)	

		return

	# Placeholder method. Intended future purpose is to open previously saved CSV data and plot it.
	def openFile(self):
		self.status_bar.showMessage('Open CSV Data clicked! Method openFile() only prints this message for now.', self.config.dict['status_bar_timeout'])

	# Saves GUI settings in a JSON file.
	def saveSettings(self):
		options = QFileDialog.Options()
		file_name, _ = QFileDialog.getSaveFileName(self,'Save Routine Settings', '',"All Files (*);;JSON (JavaScript Object Notation) (*.json)", options=options)
		if file_name:
			if file_name[-5:] != '.json':
				file_name += '.json'
			self.status_bar.showMessage(f'Saved routine settings as: {file_name}', self.config.dict['status_bar_timeout'])
			writer = JSONwriter(file_name)
			right_wdg = self.central_wdg.right_wdg
			writer.dict = {
				'azimuth' : {
					'resolution' : right_wdg.azimuth_res_combo.currentText(),
					'accel_period': right_wdg.Pa_spinbox.value(),
					'max_delay' : right_wdg.Tas_spinbox.value(),
					'min_delay' : right_wdg.Tai_spinbox.value(),
					'angle'		: right_wdg.angle_azim_spinbox.value(),
					'initial_angle' : right_wdg.initial_azim_spinbox.value(),
					'final_angle'	: right_wdg.final_azim_spinbox.value(),
					'rotations'		: right_wdg.rotations_per_elev_spinbox.value()
				},
				'elevation' : {
					'resolution' : right_wdg.elevation_res_combo.currentText(),
					'angle' : right_wdg.angle_elev_spinbox.value(),
					'initial_angle' : right_wdg.initial_elev_spinbox.value(),
					'final_angle'	: right_wdg.final_elev_spinbox.value()
				}
			}
			writer.writeJSON()
	
	# Opens previously saved JSON GUI settings file.
	def openSettings(self):
		options = QFileDialog.Options()
		file_name, _ = QFileDialog.getOpenFileName(self, 'Open Routine Settings', '', 'JSON (JavaScript Object Notation) (*.json)',  options=options)
		if file_name:
			self.status_bar.showMessage(f'Opened routine settings: {file_name}', self.config.dict['status_bar_timeout'])
			reader = JSONreader(file_name).dict
			right_wdg = self.central_wdg.right_wdg
			# Azimuth
			rdr_azim = reader['azimuth']
			right_wdg.azimuth_res_combo.setCurrentText(rdr_azim['resolution'])
			right_wdg.Pa_spinbox.setValue(rdr_azim['accel_period'])
			right_wdg.Tas_spinbox.setValue(rdr_azim['max_delay'])
			right_wdg.Tai_spinbox.setValue(rdr_azim['min_delay'])
			right_wdg.angle_azim_spinbox.setValue(rdr_azim['angle'])
			right_wdg.initial_azim_spinbox.setValue(rdr_azim['initial_angle'])
			right_wdg.final_azim_spinbox.setValue(rdr_azim['final_angle'])
			right_wdg.rotations_per_elev_spinbox.setValue(rdr_azim['rotations'])
			# Elevation
			rdr_elev = reader['elevation']
			right_wdg.elevation_res_combo.setCurrentText(rdr_elev['resolution'])
			right_wdg.angle_elev_spinbox.setValue(rdr_elev['angle'])
			right_wdg.initial_elev_spinbox.setValue(rdr_elev['initial_angle'])
			right_wdg.final_elev_spinbox.setValue(rdr_elev['final_angle'])

			#Apply changes
			self.central_wdg.applyParameters()
			
	# Opens PDF progress report in browser. 
	def helpContent(self):
		link = 'https://github.com/Zimrahin/Stepper-Motor-Controller2/blob/main/Progress_Report_CCTVal_ENG.pdf'
		QDesktopServices.openUrl(QUrl(link))

	# Opens window with general info about the software. 
	def about(self):
		description = 'A simple Graphical User interface made to communicate with a microcontroller via a serial port to control the azimuth and elevation positions of an antenna and plot the power measured at each position.'
		authors = f'{self.config.dict["authors"][0]}\n\t{self.config.dict["authors"][1]}'
		text =	f"{description}\n\nBy:\t{authors}\nVersion:\t{self.config.dict['version']}\nMade with:\tPySide2"
		informationBox(text, 'Stepper Motor Controller', 'Stepper Motor Controller').exec_()
	
	def _connectActions(self):
		# Connect File actions
		self.save_action.triggered.connect(self.saveFile)
		self.exit_action.triggered.connect(self.close)
		self.save_settings.triggered.connect(self.saveSettings)
		self.open_action.triggered.connect(self.openFile)
		self.open_settings.triggered.connect(self.openSettings)

		# Connect Help actions
		self.help_contentAction.triggered.connect(self.helpContent)
		self.about_action.triggered.connect(self.about)

	# Sets GUI fonts and colours
	def _setStyleSheet(self):
		self.setStyleSheet(f"""
							QMenuBar {{
								font: {self.config.dict['font']['text_size']}pt "{self.config.dict['font']['family']}";
								background-color: {self._palette['face_color']}; 
								color: white; 
						   	}}
							QMenu::separator {{
								background: {self._palette['start_btn']};
								height: 1px;
								margin: 4px 0px 4px 0px;
							}}
							QStatusBar {{
								font: {self.config.dict['font']['text_size']}pt "{self.config.dict['font']['family']}";
								background-color: {self._palette['face_color']}; 
								color: white; 
						   	}}
							QLabel {{
								font: {self.config.dict['font']['text_size']}pt "{self.config.dict['font']['family']}";
							}}
							QPushButton{{
								font: {self.config.dict['font']['text_size']}pt "{self.config.dict['font']['family']}";
							}}
							QComboBox{{
								font: {self.config.dict['font']['text_size']}pt "{self.config.dict['font']['family']}";
							}}
							QSpinBox{{
								font: {self.config.dict['font']['text_size']}pt "{self.config.dict['font']['family']}";
							}}
							QDoubleSpinBox{{
								font: {self.config.dict['font']['text_size']}pt "{self.config.dict['font']['family']}";
							}}
							QToolTip {{
								font: {self.config.dict['font']['title_size']}pt "{self.config.dict['font']['family']}";
								background-color: {self._palette['tooltip_background']}; 
								color: {self._palette['tooltip_colour']}; 
								border: black solid 1px
						   	}}
						   	""")

class informationBox(QMessageBox):
	def __init__(self, info: str, title: str, subtitle: str, parent=None):
		super().__init__(parent)
		self.setWindowIcon(QtGui.QIcon('img/logo.png'))
		self.setIcon(QMessageBox.Information)
		self.setText('<b>'+subtitle+'</b>')
		self.setInformativeText(info)
		self.setWindowTitle(title)
		self.setMinimumWidth(1000)


if __name__ == '__main__':
	app = QApplication([])
	app.setStyle('fusion') 
	dict = JSONreader('palette.json')
	dict = dict.dict
	palette = darkPalette(dict)
	app.setPalette(palette)
	win = mainWindow()
	# print(win.dumpObjectTree())
	win.show()

	sys.exit(app.exec_())


