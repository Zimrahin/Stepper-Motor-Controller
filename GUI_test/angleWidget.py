import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout, QFormLayout, QVBoxLayout, QRadioButton, QDoubleSpinBox, QLabel
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from math import floor

# Constants for operation
# -> Angle parameters: degree
LOWEST_DEG = 0 
HIGHEST_DEG = 360*40  # 40 revs
STEP_INCREMENT = 10
USE_DECIMALS = 2
DEG_UNITS = '\u00b0'

class angleWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		# Objects

		# Widgets       
		# -> Spinboxes
		self.angle_spinbox = QDoubleSpinBox()

		# -> Radio buttons
		self.a_radio = QRadioButton()
		self.l_radio = QRadioButton()
		self.r_radio = QRadioButton()

		self.setStyleSheet("""QToolTip { 
                           background-color: #252525; 
                           color: white; 
                           border: black solid 1px
                           }""")

		self.a_radio.setIcon(QIcon('protractor.png'))
		self.a_radio.setIconSize(QSize(90,60))
		self.a_radio.setFixedSize(90,60)
		self.a_radio.setToolTip('Move to an <b>absolute</b> angle')

		self.l_radio.setIcon(QIcon('counterclockwise.png'))
		self.l_radio.setIconSize(QSize(90,60))
		self.l_radio.setFixedSize(90,60)
		self.l_radio.setToolTip('Move <b>counterclockwise</b>')

		self.r_radio.setIcon(QIcon('clockwise.png'))
		self.r_radio.setIconSize(QSize(90,60))
		self.r_radio.setFixedSize(90,60)
		self.r_radio.setToolTip('Move <b>clockwise</b>')

		# -> Bottom buttons
		self.send_btn = QPushButton('Send')

        # -> Output text
		# self.out_label = QLabel("")

		# Init routine 
		self.angleBoxConfig(self.angle_spinbox)
		self.a_radio.setChecked(True)

		# Signals and slots
		self.send_btn.clicked.connect(self.sendParameters)

		# Layout
		v_layout = QVBoxLayout()

		# -> Boxes
		param_fields = QFormLayout()
		param_fields.addRow('Angle', self.angle_spinbox)
		v_layout.addLayout(param_fields)

		# -> Radio buttons
		radio_btn_row = QHBoxLayout()
		radio_btn_row.addWidget(self.a_radio)
		radio_btn_row.addWidget(self.l_radio)
		radio_btn_row.addWidget(self.r_radio)
		v_layout.addLayout(radio_btn_row)

		# -> Bottom buttons
		btn_row = QHBoxLayout()
		btn_row.addWidget(self.send_btn)
		v_layout.addLayout(btn_row)

        # -> Output text label widget
		# v_layout.addWidget(self.out_label)

		self.setLayout(v_layout)

	def angleBoxConfig(self, box):
		box.setMinimum(LOWEST_DEG)
		box.setMaximum(HIGHEST_DEG)
		box.setSingleStep(STEP_INCREMENT)
		box.setSuffix(DEG_UNITS)

	def sendParameters(self):
		out_angle = self.angle_spinbox.value()
		out_step = self.angleToStep(out_angle, int(self.parent().param_wdg.param_dict['Nrev']))
		listLetters = ['a', 'l', 'r']
		listRadioBtn = [self.a_radio, self.l_radio, self.r_radio]
		for i in range(len(listRadioBtn)):
			if listRadioBtn[i].isChecked():
				# self.out_label.setText(listLetters[i] + str(out_step))
				self.parent().connection_wdg.send2COM(listLetters[i] + str(out_step))
		self.parent().connection_wdg.receiveFromCOM()

	def angleToStep(self, angle, N_rev):
		step = int(floor(angle * N_rev / 360))
		return step	
		  
	def colorSpin(self, spin, color='#f86e6c'):
		spin.setStyleSheet('background-color : {};'.format(color))

if __name__ == '__main__':
	app = QApplication([])
	widget = angleWidget()
	widget.show()
	sys.exit(app.exec_())