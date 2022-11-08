import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSignal

class GreenWidget(QWidget):
    select = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)

        # Objects 
        self.leftchannel = QPushButton('Left')
        self.rightchannel = QPushButton('Right')

        # Init
        self.leftchannel.setFlat(True)

        # Signal and Slots
        self.leftchannel.clicked.connect(self.left)
        self.rightchannel.clicked.connect(self.right)


        # Layout
        layout = QHBoxLayout()

        layout.addWidget(self.leftchannel)
        layout.addWidget(self.rightchannel)

        self.setLayout(layout)

    def left(self):
        self.select.emit(0)
        self.rightchannel.setFlat(False)
        self.leftchannel.setFlat(True)        

    def right(self):
        self.select.emit(1)
        self.rightchannel.setFlat(True)
        self.leftchannel.setFlat(False)


if __name__ == '__main__':
    app = QApplication([])
    widget = GreenWidget()
    widget.show()
    sys.exit(app.exec_())