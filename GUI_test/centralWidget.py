import sys 
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtGui import QPalette, QColor, QPixmap

from connectionWidget import connectionWidget
from paramWidget import paramWidget
from angleWidget import angleWidget
from plotWidget import plotWidget

# https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
import ctypes
myappid = 'StepperMotorController' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class centralWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowIcon(QtGui.QIcon('logo.png'))
		self.setWindowTitle("Stepper motor controller")

		#Objects 
		self.COM = None


		# Widgets
		# -> Serial Connection Widget
		self.connection_wdg = connectionWidget(self)
		
		# -> Parameters Widget
		self.param_wdg = paramWidget(self)

		# -> Angle Widget
		self.angle_wdg = angleWidget(self)

		# -> Plot Widget
		self.plot_wdg = plotWidget(self)

		# -> Logo Widget
		self.logo_wdg = logoWidget(self)

		# Init routines
		self.param_wdg.setEnabled(False)
		self.angle_wdg.setEnabled(False)

		# Signals and Slots
		self.connection_wdg.connect_signal.connect(self.connectUnlock)
		self.connection_wdg.disconnect_signal.connect(self.disconnectLock)

		# Layout
		v_layout = QVBoxLayout()
		
		v_layout.addWidget(self.connection_wdg)
		v_layout.addWidget(self.param_wdg)
		v_layout.addWidget(self.angle_wdg)
		v_layout.addStretch()
		v_layout.addWidget(self.logo_wdg)
		

		h_layout = QHBoxLayout()
		h_layout.addWidget(self.plot_wdg, 5)
		h_layout.addLayout(v_layout, 1)

		self.setLayout(h_layout)

	def disconnectLock(self):
		self.COM = None
		self.param_wdg.setEnabled(False)
		self.angle_wdg.setEnabled(False)

	def connectUnlock(self):
		self.COM = self.connection_wdg.serial_COM
		self.param_wdg.setEnabled(True)
		self.angle_wdg.setEnabled(True)


class logoWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.logo_wdg = QLabel()
		self.img = QPixmap('logo2.png')
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
	palette.setColor(QPalette.ToolTipText, Qt.white)
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
		
	widget = centralWidget()
	widget.show()

	sys.exit(app.exec_())