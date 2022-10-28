# Fields to control the test
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout, QFormLayout, QVBoxLayout, QRadioButton, QSpinBox, QComboBox
from PyQt5.QtCore import pyqtSignal
import math
import numpy as np
from MessageBox import WarningBox

# Constants for operation
# -> Pa parameters: steps
LOWEST_PA = 0 
HIGHEST_PA = 1000
STEP_INCREMENT = 10
PA_UNITS = '\t step'
PA_TOLERANCE = STEP_INCREMENT/10.0


# -> Time parameters: microseconds
MIN_TIME_STEP = 0 # us
MAX_TIME_STEP = 2000 # us
TIME_STEP_INCREMENT = 10
TIME_UNITS = '\t \u03BCs'


class paramFields(QWidget):
    start_signal = pyqtSignal()
    stop_signal = pyqtSignal()
    abort_signal = pyqtSignal()

    def __init__(self, parent=None):
        
        super().__init__(parent)

        # Objects
        self.step_route = None
        self.status = True
        self.verifed = True

        # Widgets
        # -> Combo boxes
        self.Nrev_combo = QComboBox()
        self.Nrev_combo.addItems(['200','400','800','1600','3200','6400'])
        
        # -> Spinboxes
        self.Pa_spinbox = QSpinBox()
        self.Tas_spinbox = QSpinBox()
        self.Tai_spinbox = QSpinBox()

        # -> Radio buttons
        self.degree_radio = QRadioButton('Degree')
        self.step_radio = QRadioButton('Step')

        # -> Bottom buttons
        self.reset_btn = QPushButton('Reset')
        self.apply_btn = QPushButton('Apply')

        # -> list of lockable fields
        self.fields = [self.Pa_spinbox, self.Tas_spinbox, self.Tai_spinbox]

        # Init routine 
        self.SPBoxConfig(self.Pa_spinbox)
        self.apply_btn.setEnabled(True)
        self.TimeBoxConfig(self.Tai_spinbox)
        self.TimeBoxConfig(self.Tas_spinbox)

        # Signals and slots
        self.reset_btn.clicked.connect(self.verify)
        self.apply_btn.clicked.connect(self.StartStopHandler)

        self.Pa_spinbox.valueChanged.connect(self.fieldsChanged)
        self.Tas_spinbox.valueChanged.connect(self.fieldsChanged)
        self.Tai_spinbox.valueChanged.connect(self.fieldsChanged)


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

        self.setLayout(v_layout)

        
    def SPBoxConfig(self, box):
        box.setMinimum(LOWEST_PA)
        box.setMaximum(HIGHEST_PA)
        box.setSingleStep(STEP_INCREMENT)
        box.setSuffix(PA_UNITS)


    def TimeBoxConfig(self,box):
        box.setMinimum(MIN_TIME_STEP)
        box.setMaximum(MAX_TIME_STEP)
        box.setSingleStep(TIME_STEP_INCREMENT)
        #box.setDecimals(TIME_DECIMALS)
        box.setSuffix(TIME_UNITS)

    def getFieldsValues(self):
        ret_dict = {
            'initial':self.Nrev_spinbox.value(),
            'final':self.Pa_spinbox.value(),
            'sp_step':self.Tas_spinbox.value(),
            'time_step':self.Tai_spinbox.value()
        }
        return ret_dict

    def colorSpin(self, spin, color='#f86e6c'):
        spin.setStyleSheet('background-color : {};'.format(color))

    def fieldsChanged(self):
        # If any of the controls fields change and the last values were verified, lock everything as start
        if(self.verifed):
            self.verifed = not self.verifed
            self.apply_btn.setEnabled(False)

        else:
            return

    def verify(self):
        values = self.getFieldsValues()
        
        delta_sp = values['final'] - values['initial']

        # Check if Initial and Final SP are over SP_TOLERANCE
        if (math.isclose(delta_sp, 0.0, rel_tol = PA_TOLERANCE, abs_tol = 0.0)):
            self.colorSpin(self.Nrev_spinbox)
            self.colorSpin(self.Pa_spinbox)
            warning_msg = WarningBox('Initial and Final SP rates are too close, less than tolerance: {}'.format(PA_TOLERANCE), self)
            warning_msg.exec_()
            self.colorSpin(self.Nrev_spinbox, color='')
            self.colorSpin(self.Pa_spinbox, color='')
            return

        steps = np.sign(delta_sp)*values['sp_step']
        f_steps = delta_sp/steps # Needed steps
        n_steps = math.floor(f_steps) # Complete steps 
        last_flag = False


        # Check if required steps are factible
        last_step = 0.0
        if not (math.isclose(f_steps, n_steps, rel_tol=PA_TOLERANCE, abs_tol=0.0)):
            last_step = delta_sp - n_steps*steps
            last_flag = True

        # Generate steps for thread
        step_list = []
        # 1- Initial point
        step_list.append(values['initial'])

        # 2- Generate steps
        i_step = values['initial']
        for i in range(n_steps):
            i_step += steps
            step_list.append(i_step)

        # 3- Add last step if necessary
        if(last_flag):
            i_step += last_step
            step_list.append(i_step)        

        self.step_route = {
            'initial':values['initial'],
            'final':values['final'],
            'delta_sp':delta_sp,
            'n_steps':n_steps,
            'step_size':steps,
            'last_flag':last_flag,
            'last_step':last_step,
            'time_step':values['time_step'],
            'step_list':step_list
        }

        # If everything checks, enable start button
        self.verifed = True
        self.apply_btn.setEnabled(True)

    def StartStopHandler(self):
        # Check button status
        btn_status = self.apply_btn.text()
        
        if btn_status == 'Start':
            btn_text = 'Stop'
            self.reset_btn.setEnabled(False)
            self.start_signal.emit()

        else:
            btn_text = 'Start'
            self.reset_btn.setEnabled(True)
            self.stop_signal.emit()

        self.apply_btn.setText(btn_text)


    def stopHandler(self):
        self.reset_btn.setEnabled(True)
        self.apply_btn.setEnabled(True)

    def getRoute(self):
        return self.step_route

    def lockFields(self):
        self.status = not self.status

        for item in self.fields:
            item.setEnabled(self.status)


    # AGREGADO 28-10-2022
    def getNrev(self):
        return self.Nrev_combo.currentText()        

if __name__ == '__main__':
    app = QApplication([])
    widget = paramFields()
    widget.show()
    sys.exit(app.exec_())