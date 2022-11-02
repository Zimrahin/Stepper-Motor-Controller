import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout, QFormLayout, QVBoxLayout, QRadioButton, QDoubleSpinBox
from PyQt5.QtCore import pyqtSignal
import math
import numpy as np
from MessageBox import warningBox

# Constants for operation
# -> Angle parameters: degree
LOWEST_DEG = 0 
HIGHEST_DEG = 360*40
STEP_INCREMENT = 10
USE_DECIMALS = 2
DEG_UNITS = '\u00b0'
DEG_TOLERANCE = STEP_INCREMENT/10.0


class angleWidget(QWidget):
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
        #         
        # -> Spinboxes
        self.msg_spinbox = QDoubleSpinBox()

        # -> Radio buttons
        self.a_radio = QRadioButton('Absolute')
        self.l_radio = QRadioButton('Counterclockwise')
        self.r_radio = QRadioButton('Clockwise')

        # -> Bottom buttons
        self.send_btn = QPushButton('Send')

        # -> list of lockable fields
        self.fields = [self.msg_spinbox]

        # Init routine 
        self.SPBoxConfig(self.msg_spinbox)

        # Signals and slots
        self.send_btn.clicked.connect(self.verify)

        self.msg_spinbox.valueChanged.connect(self.fieldsChanged)

        # Layout
        v_layout = QVBoxLayout()

        # -> Boxes
        param_fields = QFormLayout()
        param_fields.addRow('Angle', self.msg_spinbox)
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

        self.setLayout(v_layout)

        
    def SPBoxConfig(self, box):
        box.setMinimum(LOWEST_DEG)
        box.setMaximum(HIGHEST_DEG)
        box.setSingleStep(STEP_INCREMENT)
        box.setSuffix(DEG_UNITS)


    def TimeBoxConfig(self,box):
        box.setMinimum(MIN_TIME_STEP)
        box.setMaximum(MAX_TIME_STEP)
        box.setSingleStep(TIME_STEP_INCREMENT)
        #box.setDecimals(TIME_DECIMALS)
        box.setSuffix(TIME_UNITS)

    def getFieldsValues(self):
        ret_dict = {
            'initial':self.Nrev_spinbox.value(),
            'final':self.msg_spinbox.value(),
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
        else:
            return

    def verify(self):
        values = self.getFieldsValues()
        
        delta_sp = values['final'] - values['initial']

        # Check if Initial and Final SP are over SP_TOLERANCE
        if (math.isclose(delta_sp, 0.0, rel_tol = SP_TOLERANCE, abs_tol = 0.0)):
            self.colorSpin(self.Nrev_spinbox)
            self.colorSpin(self.msg_spinbox)
            warning_msg = warningBox('Initial and Final SP rates are too close, less than tolerance: {}'.format(SP_TOLERANCE), self)
            warning_msg.exec_()
            self.colorSpin(self.Nrev_spinbox, color='')
            self.colorSpin(self.msg_spinbox, color='')
            return

        steps = np.sign(delta_sp)*values['sp_step']
        f_steps = delta_sp/steps # Needed steps
        n_steps = math.floor(f_steps) # Complete steps 
        last_flag = False


        # Check if required steps are factible
        last_step = 0.0
        if not (math.isclose(f_steps, n_steps, rel_tol=SP_TOLERANCE, abs_tol=0.0)):
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
            self.send_btn.setEnabled(False)
            self.start_signal.emit()

        else:
            btn_text = 'Start'
            self.send_btn.setEnabled(True)
            self.stop_signal.emit()

        self.apply_btn.setText(btn_text)


    def stopHandler(self):
        self.send_btn.setEnabled(True)
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
    widget = angleWidget()
    widget.show()
    sys.exit(app.exec_())