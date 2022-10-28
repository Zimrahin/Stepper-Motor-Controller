# The required control fields to setup the serial connection
import sys
from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QLabel, QApplication, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import serial
import serial.tools.list_ports
from MessageBox import ErrorBox, WarningBox, InformationBox

# Default values
CONNECTION_STATUS_LABEL = 'Connection status {}'
SERIAL_TIMEOUT = 1.0 # 1 second
TEST_CMD = b'azi\r'

class connectionFields(QWidget):

    # Class Signals
    connect_signal = QtCore.pyqtSignal()
    disconnect_signal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        
        super().__init__(parent)

        # Objects
        self.serial_comms = None

        # Widgets 
        self.serial_ports = QComboBox()
        self.refresh_btn = QPushButton('Refresh')
        self.connect_btn = QPushButton('Connect')
        self.status_label = QLabel(CONNECTION_STATUS_LABEL.format('Not Connected'))

        # Init routines
        self.status_label.setAlignment(Qt.AlignCenter)
        self.SerialList()

        # Signals and slots
        self.refresh_btn.clicked.connect(self.SerialList)
        self.connect_btn.clicked.connect(self.ConnectionHandler)

        # Widget Layout
        layout = QHBoxLayout()
        layout.addWidget(self.serial_ports)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.connect_btn)
        layout.addWidget(self.status_label)

        self.setLayout(layout)



    def SerialList(self):
        # Clear combobox 
        self.serial_ports.clear()

        # Get list of available ports
        show_ports = []
        ports = serial.tools.list_ports.comports()
        for port, _, _ in sorted(ports):
            show_ports.append(port)

        # If no ports found disable connect button
        if(len(show_ports) == 0):
            self.connect_btn.setEnabled(False)
            return
        else:
            # Add ports to combobox
            self.serial_ports.addItems(show_ports)
            # Enable connect button
            self.connect_btn.setEnabled(True)


    def ConnectionHandler(self):
        port = self.serial_ports.currentText()
        if not(port):
            # No port is selected
            warning = WarningBox('No port was found. Try refreshing')
            warning.exec_()
            return 

        try:
            if self.serial_comms:
                self.serial_comms.close()
                self.serial_comms = None
                self.disconnect_signal.emit()
                connect_btn_text = 'Connect'
                status_label_text = 'Not Connected'
                port_list_refresh_enable = True
            else:
                self.serial_comms = serial.Serial(port, timeout=SERIAL_TIMEOUT)
                self.ConnectionTest()
                self.connect_signal.emit()
                connect_btn_text = 'Disconnect'
                status_label_text = 'Connected'
                port_list_refresh_enable = False
            self.connect_btn.setText(connect_btn_text)
            self.status_label.setText(CONNECTION_STATUS_LABEL.format(status_label_text))
            self.serial_ports.setEnabled(port_list_refresh_enable)
            self.refresh_btn.setEnabled(port_list_refresh_enable)
        except Exception as e:
            self.serial_comms.close()
            self.serial_comms = None
            self.serial_ports.setEnabled(True)
            self.refresh_btn.setEnabled(True)
            show_error = ErrorBox(e, self)
            show_error.exec_()

    def ConnectionTest(self):
        self.serial_comms.write(TEST_CMD)
        response = self.serial_comms.readline()
        response = response.decode('utf-8').strip().split(',')
        if (response[0] == 'AZ' and response[3] == 'Brooks Instrument'):
            return True

        else:
            raise Exception('Device did not respond to <AZI> command')

    def getComms(self):
        return self.serial_comms



if __name__ == '__main__':
    app = QApplication([])
    widget = connectionFields()
    widget.show()
    sys.exit(app.exec_())