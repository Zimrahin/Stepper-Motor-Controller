import sys
from PySide2.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout, QFormLayout, QVBoxLayout, QSpinBox, QComboBox, QLabel
from PySide2.QtGui import QIcon, QPixmap
import PySide2.QtCore
from PySide2.QtCore import Qt

# Constants for operation
# -> Pa parameters: steps
LOWEST_PA = 0 
HIGHEST_PA = 10000
STEP_INCREMENT = 10
PA_UNITS = ' step'

# -> Time parameters: microseconds
MIN_TIME_STEP = 0 # us
MAX_TIME_STEP = 2000 # us
TIME_STEP_INCREMENT = 10
TIME_UNITS = ' \u03BCs'

STATUS_BAR_TIMEOUT = 5000

class paramWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.font_dict = {
					"family" : "Segoe UI",
					"title_size" : 14
					}

		# Widgets
		# -> Labels
		self.azimuth_txt = QLabel('<b>Azimuth Settings</b>')
		self.azimuth_txt.setStyleSheet(f"font : {self.font_dict['title_size']}pt '{self.font_dict['family']}';")
		self.azimuth_img = QLabel()
		self.img = QPixmap('img/azimuth.png')
		self.img = self.img.scaled(250, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
		self.azimuth_img.setPixmap(self.img)

		# -> Combo boxes
		self.Nrev_combo = QComboBox()
		self.Nrev_list = ['1.8 degree/step','0.9 degree/step','0.45 degree/step','0.225 degree/step','0.1125 degree/step','0.05625 degree/step']
		self.Nrev_combo.addItems(self.Nrev_list)
		
		# -> Spinboxes
		self.Pa_spinbox = QSpinBox()
		self.Tas_spinbox = QSpinBox()
		self.Tai_spinbox = QSpinBox()

		# -> Bottom buttons
		self.default_btn = QPushButton('Default')
		self.apply_btn = QPushButton('Apply')

		# Init routine 
		self.Nrev_combo.setCurrentText(self.Nrev_list[5])
		self.NBoxConfig(self.Pa_spinbox)
		self.TimeBoxConfig(self.Tai_spinbox)
		self.TimeBoxConfig(self.Tas_spinbox)

		# Objects
		self.param_dict = self.getFieldsValues()

		# Signals 
		self.default_btn.clicked.connect(self.resetParameters)
		self.apply_btn.clicked.connect(self.sendParameters)
		self.connect(self.Nrev_combo, PySide2.QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.resetParameters)

		# Layout
		v_layout = QVBoxLayout()

		# -> Title Label
		h_layout = QHBoxLayout()
		h_layout.addWidget(self.azimuth_img)
		h_layout.addWidget(self.azimuth_txt)
		h_layout.addStretch()
		v_layout.addLayout(h_layout)

		# -> Boxes
		param_fields = QFormLayout()
		param_fields.addRow('Azimuth resolution', self.Nrev_combo)
		param_fields.addRow('Acceleration period', self.Pa_spinbox)
		param_fields.addRow('Maximum added delay', self.Tas_spinbox)
		param_fields.addRow('Minimum added delay', self.Tai_spinbox)
		v_layout.addLayout(param_fields)

		# Tooltips
		self.Nrev_combo.setToolTip('Angular resolution')
		self.Pa_spinbox.setToolTip('Number of steps <b>between \nminimum</b> added delay and <b>\nmaximum</b> added delay')
		self.Tas_spinbox.setToolTip('<b>Maximum delay</b> added to <b>each step</b> \n to decrease rotation speed')
		self.Tai_spinbox.setToolTip('<b>Minimum delay</b> added to <b>each step</b> \n to decrease rotation speed')
		self.default_btn.setToolTip('Set optimum empirical parameters to <b>maximise</b> rotation speed while keeping a <b>stable behaviour</b> of stepper motor')
		self.apply_btn.setToolTip('Send command to set parameters')

		# -> Bottom buttons
		btn_row = QHBoxLayout()
		btn_row.addWidget(self.default_btn)
		btn_row.addWidget(self.apply_btn)
		v_layout.addLayout(btn_row)


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
			'Nrev':int(360/float(self.Nrev_combo.currentText().split()[0])),
			'Pa':self.Pa_spinbox.value(),
			'Tas':self.Tas_spinbox.value(),
			'Tai':self.Tai_spinbox.value()
		}
		return ret_dict

	def colorSpin(self, spin, color='#f86e6c'):
		spin.setStyleSheet('background-color : {};'.format(color))
		  
	def sendParameters(self):
		out_dict = self.getFieldsValues()
		out_string = 'p-' + str(out_dict['Nrev']) + '-' + str(out_dict['Pa']) + '-' + str(out_dict['Tas']) + '-' + str(out_dict['Tai'])  + '\n'
		# self.out_label.setText(out_string)
		# print(out_string)
		self.parent().connection_wdg.send2COM(out_string)
		
		response = self.parent().connection_wdg.receiveOnlyCOM()
		if (response == 'ack'):
			self.param_dict = out_dict #update necessary for degree->step conversion (called from angleWidget)
			# receivedSuccessBox('Parameters set successfully!').exec_()
			self.parent().parent().status_bar.showMessage("Parameters set successfully!", STATUS_BAR_TIMEOUT)
			return True
		else:
			raise Exception('Device did not respond')

	def resetParameters(self):
		if self.Nrev_combo.currentText() == self.Nrev_list[5]:
			self.Pa_spinbox.setValue(0)
			self.Tas_spinbox.setValue(0)
			self.Tai_spinbox.setValue(0)
		elif self.Nrev_combo.currentText() == self.Nrev_list[4]:
			self.Pa_spinbox.setValue(0)
			self.Tas_spinbox.setValue(0)
			self.Tai_spinbox.setValue(0)
		elif self.Nrev_combo.currentText() == self.Nrev_list[3]:
			self.Pa_spinbox.setValue(800)
			self.Tas_spinbox.setValue(8)
			self.Tai_spinbox.setValue(0)
		elif self.Nrev_combo.currentText() == self.Nrev_list[2]:
			self.Pa_spinbox.setValue(800)
			self.Tas_spinbox.setValue(16)
			self.Tai_spinbox.setValue(8)
		elif self.Nrev_combo.currentText() == self.Nrev_list[1]:
			self.Pa_spinbox.setValue(800)
			self.Tas_spinbox.setValue(20)
			self.Tai_spinbox.setValue(12)
		elif self.Nrev_combo.currentText() == self.Nrev_list[0]:
			self.Pa_spinbox.setValue(800)
			self.Tas_spinbox.setValue(22)
			self.Tai_spinbox.setValue(14)
		else:
			print('if you see this, there is an error (probably)')
			  

if __name__ == '__main__':
	app = QApplication([])
	widget = paramWidget()
	widget.show()
	sys.exit(app.exec_())