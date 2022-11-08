import sys
from PySide2.QtWidgets import QVBoxLayout, QApplication, QWidget, QLabel
from PySide2.QtGui import QPixmap, QPainter

class imgResize(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent=parent)
		self.p = QPixmap()
		# self.p.resize(440, 330)


	def setPixmap(self, p):
		self.p = p
		self.update()

	def paintEvent(self, event):
		if not self.p.isNull():
			painter = QPainter(self)
			painter.setRenderHint(QPainter.SmoothPixmapTransform)
			painter.drawPixmap(self.rect(), self.p)

class plotWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		# Objects 
		self.img = imgResize(self)

		# Object init 
		self.img.setPixmap(QPixmap('img/osc.png'))
		# self.resize(440, 330)
		# self.resize(self.sizeHint())
		self.setMinimumWidth(600)
		self.setMinimumHeight(330)

		# Signal and Slots

		# Layout
		layout = QVBoxLayout()
		layout.addWidget(self.img)
		
		self.setLayout(layout)


if __name__ == '__main__':
	app = QApplication([])
	widget = plotWidget()
	# widget.resize(440, 330)
	widget.show()
	sys.exit(app.exec_())