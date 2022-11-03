import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout, QFormLayout, QVBoxLayout, QRadioButton, QSpinBox, QComboBox, QLabel
from PyQt5.QtCore import pyqtSignal
import math
import numpy as np
from MessageBox import warningBox

# Constants for operation
# -> Pa parameters: steps
# LOWEST_PA = 0 
# HIGHEST_PA = 1000
# STEP_INCREMENT = 10
# PA_UNITS = '\t\t\t step'
# PA_TOLERANCE = STEP_INCREMENT/10.0

# -> Time parameters: microseconds
# MIN_TIME_STEP = 0 # us
# MAX_TIME_STEP = 2000 # us
# TIME_STEP_INCREMENT = 10
# TIME_UNITS = '\t\t\t \u03BCs'

class paramWidget(QWidget):
    start_signal = pyqtSignal()
    stop_signal = pyqtSignal()
    abort_signal = pyqtSignal()

    def __init__(self, parent=None):
        
        super().__init__(parent)

        # Objects
        self.step_route = None
        self.status = True
        self.verifed = True
        # self.Nrev = 200
        # self.Pa = 0
        # self.Tai = 0
        # self.Tas = 0

        # Widgets
        # -> Combo boxes
        self.Nrev_combo = QComboBox()
        self.Nrev_combo.addItems(['200','400','800','1600','3200','6400'])
        
        # -> Spinboxes
        self.Pa_spinbox = QSpinBox()
        self.Tas_spinbox = QSpinBox()
        self.Tai_spinbox = QSpinBox()

        # -> Output text
        self.out_lbl = QLabel("")

        # -> Radio buttons
        # self.degree_radio = QRadioButton('Degree')
        # self.step_radio = QRadioButton('Step')

        # -> Bottom buttons
        self.reset_btn = QPushButton('Reset')
        self.apply_btn = QPushButton('Apply')

        # -> list of lockable fields
        self.fields = [self.Pa_spinbox, self.Tas_spinbox, self.Tai_spinbox]

        # Init routine 
        self.apply_btn.setEnabled(True)
        # self.SPBoxConfig(self.Pa_spinbox)
        # self.TimeBoxConfig(self.Tai_spinbox)
        # self.TimeBoxConfig(self.Tas_spinbox)

        # Signals and slots (¿es necesario?, ¿como se hace lo de la verificacion?)
        # self.Pa_spinbox.valueChanged.connect(self.fieldsChanged)
        # self.Tas_spinbox.valueChanged.connect(self.fieldsChanged)
        # self.Tai_spinbox.valueChanged.connect(self.fieldsChanged)

        # self.reset_btn.clicked.connect(self.verify)
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
        v_layout.addWidget(self.out_lbl)

        # -> Final layout
        self.setLayout(v_layout)

        
    # def SPBoxConfig(self, box):
    #     box.setMinimum(LOWEST_PA)
    #     box.setMaximum(HIGHEST_PA)
    #     box.setSingleStep(STEP_INCREMENT)
    #     box.setSuffix(PA_UNITS)

    # def TimeBoxConfig(self,box):
    #     box.setMinimum(MIN_TIME_STEP)
    #     box.setMaximum(MAX_TIME_STEP)
    #     box.setSingleStep(TIME_STEP_INCREMENT)
    #     #box.setDecimals(TIME_DECIMALS)
    #     box.setSuffix(TIME_UNITS)

    def getFieldsValues(self):
        ret_dict = {
            'Nrev':self.Nrev_combo.currentText(),
            'Pa':self.Pa_spinbox.value(),
            'Tas':self.Tas_spinbox.value(),
            'Tai':self.Tai_spinbox.value()
        }
        return ret_dict

    def colorSpin(self, spin, color='#f86e6c'):
        spin.setStyleSheet('background-color : {};'.format(color))

    # def fieldsChanged(self):
    #     # If any of the controls fields change and the last values were verified, lock everything as start
    #     if(self.verifed):
    #         self.verifed = not self.verifed
    #         self.apply_btn.setEnabled(False)
    #     else:
    #         return

    # def StartStopHandler(self):
    #     # Check button status
    #     btn_status = self.apply_btn.text()
        
    #     if btn_status == 'Start':
    #         btn_text = 'Stop'
    #         self.reset_btn.setEnabled(False)
    #         self.start_signal.emit()

    #     else:
    #         btn_text = 'Start'
    #         self.reset_btn.setEnabled(True)
    #         self.stop_signal.emit()

    #     self.apply_btn.setText(btn_text)

    # def stopHandler(self):
    #     self.reset_btn.setEnabled(True)
    #     self.apply_btn.setEnabled(True)

    # def getRoute(self):
    #     return self.step_route

    # def lockFields(self):
    #     self.status = not self.status

    #     for item in self.fields:
    #         item.setEnabled(self.status)


    # AGREGADO 28-10-2022
    def getNrev(self):
        return self.Nrev_combo.currentText()   
            
    # 03-11-2022:            
    def sendParameters(self):
        out_dict = self.getFieldsValues()
        out_string = 'p-' + str(out_dict['Nrev']) + '-' + str(out_dict['Pa']) + '-' + str(out_dict['Tas']) + '-' + str(out_dict['Tai']) + '\n'
        self.out_lbl.setText(out_string)
              

if __name__ == '__main__':
    app = QApplication([])
    widget = paramWidget()
    widget.show()
    sys.exit(app.exec_())