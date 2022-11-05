from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

class Window(QWidget):

	def __init__(self):
		super().__init__()
		self.flag = False


		self.button = QPushButton()
		icon = QIcon("logo2.png")
		self.button.setIcon(icon)
		self.button.setIconSize(QSize(857,289))
		self.button.setFixedSize(857,289)
		self.button.clicked.connect(self.click)

		lay = QVBoxLayout(self)
		lay.addWidget(self.button)

		self.palette = self.palette()
		self.palette.setColor(QPalette.Window, QColor(3, 18, 14))

		self.palette.setColor(QPalette.Button, QColor('red'))  

		self.setPalette(self.palette)

	def click(self):
		if not self.flag:
			self.palette.setColor(QPalette.Button, QColor(62, 80, 91))
		else: 
			self.palette.setColor(QPalette.Button, QColor(0, 0, 128))

		self.setPalette(self.palette)
		self.flag = not self.flag


if __name__ == '__main__':
	import sys
	app = QApplication([])

	app.setStyle('Fusion') 

	w = Window()
	w.show()
	sys.exit(app.exec_())