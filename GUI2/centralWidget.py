import sys 
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame, QPushButton
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
		h_layout.addWidget(self.plot_wdg, 6)
		h_layout.addLayout(v_layout, 1)

		self.setLayout(h_layout)

	def applyParameters(self):
		out_dict = self.right_wdg.getFieldsValues()
		out_string = 'p-' + str(out_dict['Nrev']) + '-' + str(out_dict['Pa']) + '-' + str(out_dict['Tas']) + '-' + str(out_dict['Tai']) + '-' + str(self.right_wdg.elev_res) + '\n'
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
		self.connection_wdg.send2COM('n4-r1600')
		while(True):
			received_string_debug = self.connection_wdg.receiveOnlyCOM()
			if received_string_debug:
				print(received_string_debug)
				continue
			else:
				break

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