# Selection of the channel of operation

import sys
from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QLabel, QApplication, QFormLayout, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

class ChannelSelection(QWidget):
    manual_signal = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # objects
        self.status = True

        # Widgets
        self.channels = QComboBox()
        self.warmup = QPushButton("Manual Warmup")

        # Init routines
        self.channels.addItems(['1','2','3','4'])

        # Signals and slots
        self.warmup.clicked.connect(self.manualWarmup)

        # Layout
        layout = QHBoxLayout()
        # Channel selection 
        channel_layout = QFormLayout()
        channel_layout.addRow('Select Channel: \t', self.channels)
        
        # Widget Layout
        layout.addLayout(channel_layout)
        layout.addWidget(self.warmup)


        self.setLayout(layout)

    def getChannel(self):
        return self.channels.currentText()

    def lockChannels(self):
        self.status = not self.status
        self.setEnabled(self.status)

    def manualWarmup(self):
        # Indicate that manual processing is being performed
        self.manual_signal.emit()

if __name__ == '__main__':
    app = QApplication([])
    widget = ChannelSelection()
    widget.show()
    sys.exit(app.exec_())