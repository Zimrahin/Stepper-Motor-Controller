from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
from PyQt5.QtGui import QPalette, QColor

class Window(QWidget):

	def __init__(self):
		super().__init__()
		self.flag = False

		self.button = QPushButton('change the colors of the buttons', self)
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