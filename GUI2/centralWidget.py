import sys 
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame
from PySide2 import QtGui
from PySide2.QtCore import Qt
from PySide2.QtGui import QPalette, QColor, QPixmap, QFont

from connectionWidget import connectionWidget
from rightWidget import rightWidget
from plotWidget import plotWidget

# https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
import ctypes
myappid = 'StepperMotorController' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class centralWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowIcon(QtGui.QIcon('img/logo.png'))
		self.setWindowTitle("Stepper motor controller")

		#Objects 
		self.COM = None
		# ------------------------------------------------------------
		# Widgets

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

		# Signals and Slots
		self.connection_wdg.connect_signal.connect(self.connectUnlock)
		self.connection_wdg.disconnect_signal.connect(self.disconnectLock)
		# ------------------------------------------------------------
		# Layout
		v_layout = QVBoxLayout()
		
		v_layout.addWidget(self.connection_wdg)
		# v_layout.addWidget(self.right_wdg)
		v_layout.addWidget(self.scroll_area)
		# v_layout.addStretch()
		v_layout.addWidget(self.logo_wdg)
		

		h_layout = QHBoxLayout()
		h_layout.addWidget(self.plot_wdg, 6)
		h_layout.addLayout(v_layout, 1)

		self.setLayout(h_layout)

	def disconnectLock(self):
		self.COM = None
		self.right_wdg.setEnabled(False)

	def connectUnlock(self):
		self.COM = self.connection_wdg.serial_COM
		self.right_wdg.setEnabled(True)


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