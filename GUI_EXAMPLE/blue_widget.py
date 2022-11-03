import sys
from PyQt5.QtWidgets import QVBoxLayout, QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap


class BlueWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		# Objects 
		self.red = QPixmap('rojo.png')
		self.blue = QPixmap('blue.png')

		self.img = QLabel()

		# Object init 
		self.img.setPixmap(self.red)

		# Signal and Slots


		# Layout
		layout = QVBoxLayout()
		layout.addWidget(self.img)
		
		self.setLayout(layout)

	def changeImg(self, value):
		if(value):
			self.img.setPixmap(self.blue)

		else:
			self.img.setPixmap(self.red)

			


if __name__ == '__main__':
	app = QApplication([])
	widget = BlueWidget()
	widget.show()
	sys.exit(app.exec_())