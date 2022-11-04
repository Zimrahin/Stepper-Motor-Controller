import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout, QFormLayout, QVBoxLayout, QSpinBox, QComboBox, QLabel

# Constants for operation
# -> Pa parameters: steps
LOWEST_PA = 0 
HIGHEST_PA = 1000
STEP_INCREMENT = 10
PA_UNITS = ' step'

# -> Time parameters: microseconds
MIN_TIME_STEP = 0 # us
MAX_TIME_STEP = 2000 # us
TIME_STEP_INCREMENT = 10
TIME_UNITS = ' \u03BCs'

class paramWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		# Objects

		# Widgets
		# -> Combo boxes
		self.Nrev_combo = QComboBox()
		self.Nrev_combo.addItems(['200 step/rev','400 step/rev','800 step/rev','1600 step/rev','3200 step/rev','6400 step/rev'])
		
		# -> Spinboxes
		self.Pa_spinbox = QSpinBox()
		self.Tas_spinbox = QSpinBox()
		self.Tai_spinbox = QSpinBox()

		# -> Output text
		self.out_label = QLabel("")

		# -> Radio buttons
		# self.degree_radio = QRadioButton('Degree')
		# self.step_radio = QRadioButton('Step')

		# -> Bottom buttons
		self.reset_btn = QPushButton('Reset')
		self.apply_btn = QPushButton('Apply')

		# Init routine 
		self.Nrev_combo.setCurrentText('6400 step/rev')
		self.NBoxConfig(self.Pa_spinbox)
		self.TimeBoxConfig(self.Tai_spinbox)
		self.TimeBoxConfig(self.Tas_spinbox)

		# Signals 
		self.reset_btn.clicked.connect(self.resetParameters)
		self.apply_btn.clicked.connect(self.sendParameters)

		# Layout
		v_layout = QVBoxLayout()

		# -> Boxes
		param_fields = QFormLayout()
		param_fields.addRow('Nrev', self.Nrev_combo)
		param_fields.addRow('Pa', self.Pa_spinbox)
		param_fields.addRow('Tas', self.Tas_spinbox)
		param_fields.addRow('Tai', self.Tai_spinbox)
		v_layout.addLayout(param_fields)

		# # -> Radio buttons
		# radio_btn_row = QHBoxLayout()
		# radio_btn_row.addWidget(self.degree_radio)
		# radio_btn_row.addWidget(self.step_radio)
		# v_layout.addLayout(radio_btn_row)

		# -> Bottom buttons
		btn_row = QHBoxLayout()
		btn_row.addWidget(self.reset_btn)
		btn_row.addWidget(self.apply_btn)
		v_layout.addLayout(btn_row)

		# -> Output text label widget
		v_layout.addWidget(self.out_label)

		# -> Final layout
		self.setLayout(v_layout)

		
	def NBoxConfig(self, box):
		box.setMinimum(LOWEST_PA)
		box.setMaximum(HIGHEST_PA)
		box.setSingleStep(STEP_INCREMENT)
		box.setSuffix(PA_UNITS)

	def TimeBoxConfig(self,box):
		box.setMinimum(MIN_TIME_STEP)
		box.setMaximum(MAX_TIME_STEP)
		box.setSingleStep(TIME_STEP_INCREMENT)
		box.setSuffix(TIME_UNITS)

	def getFieldsValues(self):
		ret_dict = {
			'Nrev':self.Nrev_combo.currentText().split()[0],
			'Pa':self.Pa_spinbox.value(),
			'Tas':self.Tas_spinbox.value(),
			'Tai':self.Tai_spinbox.value()
		}
		return ret_dict

	def colorSpin(self, spin, color='#f86e6c'):
		spin.setStyleSheet('background-color : {};'.format(color))
		  
	def sendParameters(self):
		out_dict = self.getFieldsValues()
		out_string = 'p-' + str(out_dict['Nrev']) + '-' + str(out_dict['Pa']) + '-' + str(out_dict['Tas']) + '-' + str(out_dict['Tai']) + '\n'
		self.out_label.setText(out_string)

	def resetParameters(self):
		self.Nrev_combo.setCurrentText('6400 step/rev')
		self.Pa_spinbox.setValue(0)
		self.Tai_spinbox.setValue(0)
		self.Tas_spinbox.setValue(0)
			  

if __name__ == '__main__':
	app = QApplication([])
	widget = paramWidget()
	widget.show()
	sys.exit(app.exec_())