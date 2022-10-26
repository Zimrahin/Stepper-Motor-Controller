import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from green_widget import GreenWidget
from blue_widget import BlueWidget

class RedWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Objects 
        self.green = GreenWidget(self)
        self.blue = BlueWidget(self)
        # Signal and Slots

        self.green.select.connect(self.blue.changeImg)


        # Layout
        layout = QVBoxLayout()

        layout.addWidget(self.green)
        layout.addWidget(self.blue)

        self.setLayout(layout)




if __name__ == '__main__':
    app = QApplication([])
    widget = RedWidget()
    widget.show()
    sys.exit(app.exec_())