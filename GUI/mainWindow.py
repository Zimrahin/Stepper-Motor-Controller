import sys
import time
from PySide2 import QtGui
from PySide2.QtCore import Qt, QUrl
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QMenuBar, QMenu, QAction, QFileDialog, QMessageBox
from PySide2.QtGui import QDesktopServices

from centralWidget import centralWidget
from darkPalette import darkPalette

STATUS_BAR_TIMEOUT = 5000

class Window(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.settings_dict = {
							"font" : 
							{
							"family" : "Segoe UI",
							"title_size" : 11,
							"text_size" : 9
							}
						}
		self.setWindowIcon(QtGui.QIcon('img/logo.png'))
		self.setWindowTitle("Stepper Motor Controller")

		self.setStyleSheet(f"""
							QMenuBar {{
								font: {self.settings_dict['font']['text_size']}pt "{self.settings_dict['font']['family']}";
								background-color: #191919; 
								color: white; 
								border: black solid 1px
						   	}}
							QStatusBar {{
								font: {self.settings_dict['font']['text_size']}pt "{self.settings_dict['font']['family']}";
								background-color: #191919; 
								color: white; 
								border: black solid 1px
						   	}}
							QLabel {{
								font: {self.settings_dict['font']['text_size']}pt "{self.settings_dict['font']['family']}";
							}}
							QPushButton{{
								font: {self.settings_dict['font']['text_size']}pt "{self.settings_dict['font']['family']}";
							}}
							QComboBox{{
								font: {self.settings_dict['font']['text_size']}pt "{self.settings_dict['font']['family']}";
							}}
							QSpinBox{{
								font: {self.settings_dict['font']['text_size']}pt "{self.settings_dict['font']['family']}";
							}}
							QDoubleSpinBox{{
								font: {self.settings_dict['font']['text_size']}pt "{self.settings_dict['font']['family']}";
							}}
							QToolTip {{
								font: {self.settings_dict['font']['title_size']}pt "{self.settings_dict['font']['family']}";
								background-color: #1f2126; 
								color: white; 
								border: black solid 1px
						   	}}
						   	""")


		#Objects
		self.file_name_flag = False
		self.file_name = ''

		# Widgets
		# -> Central Widget
		self.central_wdg = centralWidget(self)
		self.setCentralWidget(self.central_wdg)

		# Status Bar
		self.status_bar = self.statusBar()
		self._version = '2.11.18'
		self.permanent_message = QLabel(f'Version {self._version}')
		self.permanent_message.setStyleSheet('color : #888888')
		self.permanent_message.setAlignment(Qt.AlignRight)
		self.status_bar.addPermanentWidget(self.permanent_message)

		self._createActions()
		self._createMenuBar()
		self._connectActions()

		
	def _createMenuBar(self):
		menu_bar = QMenuBar(self)
		self.setMenuBar(menu_bar)

		fileMenu = QMenu("&File", self)#&: keyboard shortcut
		helpMenu = QMenu("&Help", self)
		menu_bar.addMenu(fileMenu)
		menu_bar.addMenu(helpMenu)

		#Actions
		fileMenu.addAction(self.saveAction)
		fileMenu.addAction(self.exitAction)

		helpMenu.addAction(self.helpContentAction)
		helpMenu.addAction(self.aboutAction)

	def _createActions(self):
		self.saveAction = QAction("&New Save File", self)
		self.exitAction = QAction("&Exit", self)

		self.helpContentAction = QAction("&Help Content", self)
		self.aboutAction = QAction("&About", self)

	def saveFile(self):
		options = QFileDialog.Options()
		# options |= QFileDialog.DontUseNativeDialog
		file_name, _ = QFileDialog.getSaveFileName(self,'Save File',time.strftime("csv_files/%d_%B_%Y_%Hh_%Mm_%Ss.csv", time.localtime()),"All Files (*);;CSV(*.csv)", options=options)
		if file_name:
			self.status_bar.showMessage(f'Selected path: {file_name}', STATUS_BAR_TIMEOUT)
			self.file_name_flag = True
			self.file_name = file_name

	def helpContent(self):
		# self.status_bar.showMessage("Help > Help Content clicked", STATUS_BAR_TIMEOUT)
		link = 'https://github.com/Zimrahin/Stepper-Motor-Controller/blob/main/Progress_Report_CCTVal_ENG.pdf'
		QDesktopServices.openUrl(QUrl(link))

	def about(self):
		# self.status_bar.showMessage("Help > About clicked", STATUS_BAR_TIMEOUT)
		description = 'A simple Graphical User interface made to communicate with a microcontroller via a serial port to control the azimuth and elevation positions of an antenna and plot the power measured at each position.'
		authors = 'Diego Badillo\n\tSebastián San Martín'
		text =	f"{description}\n\nBy:\t{authors}\nVersion:\t{self._version}\nMade with:\tPySide2"
		informationBox(text, 'Stepper Motor Controller', 'Stepper Motor Controller').exec_()
	
	def _connectActions(self):
		# Connect File actions
		# self.newAction.triggered.connect(self.newFile)
		self.saveAction.triggered.connect(self.saveFile)
		self.exitAction.triggered.connect(self.close)

		# Connect Help actions
		self.helpContentAction.triggered.connect(self.helpContent)
		self.aboutAction.triggered.connect(self.about)

class informationBox(QMessageBox):
	def __init__(self, info: str, title: str, subtitle: str, parent=None):
		super().__init__(parent)
		self.setWindowIcon(QtGui.QIcon('img/logo.png'))
		self.setIcon(QMessageBox.Information)
		self.setText('<b>'+subtitle+'</b>')
		self.setInformativeText(info)
		self.setWindowTitle(title)
		self.setMinimumWidth(1000)

# PySide2.QtWidgets.QApplication.setAttribute(PySide2.QtCore.Qt.AA_EnableHighDpiScaling, True)
if __name__ == '__main__':
	# os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "2"
	app = QApplication([])
	# app.setAttribute(PySide2.QtCore.Qt.AA_EnableHighDpiScaling)
	# if os.name == 'nt': # New Technology GUI (Windows)
	app.setStyle('fusion') 
	palette = darkPalette()
	app.setPalette(palette)

	win = Window()
	# print(win.dumpObjectTree())
	win.move(350,150)
	win.show()

	sys.exit(app.exec_())


