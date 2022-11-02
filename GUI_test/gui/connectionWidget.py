import sys
from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QLabel, QApplication, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import serial
import serial.tools.list_ports
from MessageBox import errorBox, warningBox, informationBox

# Default values
CONNECTION_STATUS_LABEL = '{}'
SERIAL_TIMEOUT = 1.0 # second (wait for Arduino response)
TEST_CMD = b'azi\r' #b: format, sendthis message to Arduino and receive aknowledge

class connectionWidget(QWidget):

    # Class Signals
    connect_signal = QtCore.pyqtSignal()
    disconnect_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        
        super().__init__(parent)

        # Objects
        self.serial_COM = None

        # Widgets 
        self.serial_ports = QComboBox()
        self.refresh_btn = QPushButton('Refresh') # refresh COMs
        self.connect_btn = QPushButton('Connect')
        self.status_label = QLabel(CONNECTION_STATUS_LABEL.format('Not connected'))

        # Init routines
        self.status_label.setAlignment(Qt.AlignCenter)
        self.serialList()

        # Signals and slots
        self.refresh_btn.clicked.connect(self.serialList)
        self.connect_btn.clicked.connect(self.connectionHandler)

        # Widget Layout
        layout = QHBoxLayout()
        layout.addWidget(self.serial_ports)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.connect_btn)
        layout.addWidget(self.status_label)

        self.setLayout(layout)



    def serialList(self):
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


    def connectionHandler(self):
        port = self.serial_ports.currentText()
        if not(port):
            # No port is selected
            warning = warningBox('No port was found. Try refreshing')
            warning.exec_()
            return 

        try:
            if self.serial_COM:
                self.serial_COM.close()
                self.serial_COM = None
                self.disconnect_signal.emit()
                connect_btn_text = 'Connect'
                status_label_text = 'Not Connected'
                port_list_refresh_enable = True
            else:
                self.serial_COM = serial.Serial(port, timeout=SERIAL_TIMEOUT)
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
            self.serial_COM.close()
            self.serial_COM = None
            self.serial_ports.setEnabled(True)
            self.refresh_btn.setEnabled(True)
            show_error = errorBox(e, self)
            show_error.exec_()

    def ConnectionTest(self):
        self.serial_COM.write(TEST_CMD)
        response = self.serial_COM.readline()
        response = response.decode('utf-8').strip().split(',')
        if (response[0] == 'AZ' and response[3] == 'Brooks Instrument'):
            return True

        else:
            raise Exception('Device did not respond to <AZI> command')

    def getComms(self):
        return self.serial_COM



if __name__ == '__main__':
    app = QApplication([])
    widget = connectionWidget()
    widget.show()
    sys.exit(app.exec_())