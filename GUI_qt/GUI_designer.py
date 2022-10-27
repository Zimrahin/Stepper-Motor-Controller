import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(0,0,200,200)
    win.setWindowTitle("hello world")

    win.show()
    sys.exit(app.exec_())

window()
