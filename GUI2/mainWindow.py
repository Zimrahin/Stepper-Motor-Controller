import sys
import time
from PySide2 import QtGui
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QMenuBar, QMenu, QToolBar, QAction, QFileDialog
from PySide2.QtGui import QPalette, QColor, QFont

from centralWidget import centralWidget

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
		self.setWindowTitle("Stepper motor controller")

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
								background-color: #252525; 
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
		self.permanent_message = QLabel('Version 2.11.18')
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
		fileMenu.addAction(self.newAction)
		fileMenu.addAction(self.saveAction)
		fileMenu.addAction(self.exitAction)

		helpMenu.addAction(self.helpContentAction)
		helpMenu.addAction(self.aboutAction)

	def _createActions(self):
		self.newAction = QAction("&New", self)
		self.saveAction = QAction("&Save", self)
		self.exitAction = QAction("&Exit", self)

		self.helpContentAction = QAction("&Help Content", self)
		self.aboutAction = QAction("&About", self)

	def newFile(self):
		self.status_bar.showMessage("File > New clicked", STATUS_BAR_TIMEOUT)

	def saveFile(self):
		options = QFileDialog.Options()
		# options |= QFileDialog.DontUseNativeDialog
		file_name, _ = QFileDialog.getSaveFileName(self,'Save File',time.strftime("csv_files/%d_%B_%Y_%Hh_%Mm_%Ss.csv", time.localtime()),"All Files (*);;CSV(*.csv)", options=options)
		if file_name:
			self.status_bar.showMessage(f'Selected path: {file_name}', STATUS_BAR_TIMEOUT)
			self.file_name_flag = True
			self.file_name = file_name

	def helpContent(self):
		self.status_bar.showMessage("Help > Help Content clicked", STATUS_BAR_TIMEOUT)

	def about(self):
		self.status_bar.showMessage("Help > About clicked", STATUS_BAR_TIMEOUT)
	
	def _connectActions(self):
		# Connect File actions
		self.newAction.triggered.connect(self.newFile)
		self.saveAction.triggered.connect(self.saveFile)
		self.exitAction.triggered.connect(self.close)

		# Connect Help actions
		self.helpContentAction.triggered.connect(self.helpContent)
		self.aboutAction.triggered.connect(self.about)


def darkMode():
	# Dark Theme
	# Adapted from https://github.com/pyqt/examples/tree/_/src/09%20Qt%20dark%20theme
	palette = QPalette()
	color1 = QColor(44, 49, 54)
	color2 = QColor(21, 23, 26)
	color3 = QColor(90, 90, 90)
	color4 = QColor(40, 43, 48)
	palette.setColor(QPalette.Window, color1)
	palette.setColor(QPalette.WindowText, Qt.white)
	palette.setColor(QPalette.Base, color2)
	palette.setColor(QPalette.AlternateBase, color1)
	palette.setColor(QPalette.ToolTipBase, Qt.black)
	palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
	palette.setColor(QPalette.Text, Qt.white)
	palette.setColor(QPalette.Button, color1)
	palette.setColor(QPalette.ButtonText, Qt.white)
	palette.setColor(QPalette.BrightText, Qt.red)
	palette.setColor(QPalette.Link, '#0ccfb9')
	palette.setColor(QPalette.Highlight, '#0ccfb9')
	palette.setColor(QPalette.HighlightedText, Qt.black)
	palette.setColor(QPalette.Disabled, QPalette.Base, color4)
	palette.setColor(QPalette.Disabled, QPalette.Text, color3)
	palette.setColor(QPalette.Disabled, QPalette.Button, QColor(33, 36, 41))
	palette.setColor(QPalette.Disabled, QPalette.ButtonText, color3)
	palette.setColor(QPalette.Disabled, QPalette.Window, color4)
	palette.setColor(QPalette.Disabled, QPalette.WindowText, color3)
	return palette


if __name__ == '__main__':
	app = QApplication([])
	# if os.name == 'nt': # New Technology GUI (Windows)
	app.setStyle('fusion') 
	palette = darkMode()
	app.setPalette(palette)
	app.setFont(QFont("Arial", 9))
		
	win = Window()
	# print(win.dumpObjectTree())
	win.move(350,150)
	win.show()

	sys.exit(app.exec_())


