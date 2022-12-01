__author__ = 'github.com/Zimrahin'

import sys
import time
from PySide2 import QtGui
from PySide2.QtCore import Qt, QUrl
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QMenuBar, QMenu, QAction, QFileDialog, QMessageBox
from PySide2.QtGui import QDesktopServices

from centralWidget import centralWidget
from darkPalette import darkPalette
from JSONreader import JSONreader

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

	def _createActions(self):
		self.save_settings = QAction("Save Routine Settings", self)
		self.open_settings = QAction('Open Routine Settings', self)
		self.save_action = QAction("New Save File", self)
		self.open_action = QAction('Open CSV data', self)
		self.exit_action = QAction("Exit", self)

		self.help_contentAction = QAction("Help Content", self)
		self.about_action = QAction("About", self)

	def saveFile(self):
		options = QFileDialog.Options()
		# options |= QFileDialog.DontUseNativeDialog
		file_name, _ = QFileDialog.getSaveFileName(self,'Save File',time.strftime("csv_files/%d_%B_%Y_%Hh_%Mm_%Ss.csv", time.localtime()),"All Files (*);;CSV (Comma delimited) (*.csv)", options=options)
		if file_name:
			if file_name[-4:] != '.csv':
				file_name += '.csv'
			self.status_bar.showMessage(f'Selected path: {file_name}', self.config.dict['status_bar_timeout'])
			# Only for CSV writing afterwards
			self.file_name_flag = True
			self.file_name = file_name

	def openFile(self):
		self.status_bar.showMessage('opeFile()', self.config.dict['status_bar_timeout'])

	def saveSettings(self):
		options = QFileDialog.Options()
		file_name, _ = QFileDialog.getSaveFileName(self,'Save File','',"All Files (*);;JSON (JavaScript Object Notation) (*.json)", options=options)
		if file_name:
			if file_name[-5:] != '.json':
				file_name += '.json'
			self.status_bar.showMessage(f'Saved routine settings as: {file_name}', self.config.dict['status_bar_timeout'])
			
	
	def openSettings(self):
		self.status_bar.showMessage('openSettings()', self.config.dict['status_bar_timeout'])



	def helpContent(self):
		link = 'https://github.com/Zimrahin/Stepper-Motor-Controller/blob/main/Progress_Report_CCTVal_ENG.pdf'
		QDesktopServices.openUrl(QUrl(link))

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


