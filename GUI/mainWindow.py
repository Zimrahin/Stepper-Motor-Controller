import sys
import time
from PySide2 import QtGui
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QMenuBar, QMenu, QToolBar, QAction, QFileDialog
from PySide2.QtGui import QPalette, QColor, QFont

from centralWidget import centralWidget

class Window(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowIcon(QtGui.QIcon('img/logo.png'))
		self.setWindowTitle("Stepper motor controller")
		self.setStyleSheet("""
							QMenuBar { 
                           	background-color: #191919; 
                           	color: white; 
                           	border: black solid 1px
                           	}
							QStatusBar { 
                           	background-color: #191919; 
                           	color: white; 
                           	border: black solid 1px
                           	}
						   	""")
		# Widgets
		# -> Central Widget
		self.central_wdg = centralWidget(self)
		self.setCentralWidget(self.central_wdg)

		# Status Bar
		self.status_bar = self.statusBar()
		self.permanent_message = QLabel('Version 1.11.09')
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
		self.status_bar.showMessage("File > New clicked", 3000)

	def saveFile(self):
		options = QFileDialog.Options()
		# options |= QFileDialog.DontUseNativeDialog
		file_name, _ = QFileDialog.getSaveFileName(self,'Save File',time.strftime("csv_files/%d_%B_%Y_%Hh_%Mm_%Ss.csv", time.localtime()),"All Files (*);;CSV(*.csv)", options=options)
		if file_name:
			print(file_name)

	def helpContent(self):
		self.status_bar.showMessage("Help > Help Content clicked", 3000)

	def about(self):
		self.status_bar.showMessage("Help > About clicked", 3000)
	
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
		
	win = Window()
	win.show()

	sys.exit(app.exec_())


