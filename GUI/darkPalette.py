from PySide2.QtCore import Qt
from PySide2.QtGui import QPalette, QColor

def darkPalette():
	# Dark Theme
	palette = QPalette()
	color1 = QColor(44, 49, 54)
	color2 = QColor(21, 23, 26)
	color3 = QColor(90, 90, 90)
	color4 = QColor(40, 43, 48)
	palette.setColor(QPalette.Window, color1)
	palette.setColor(QPalette.WindowText, Qt.white)
	palette.setColor(QPalette.Base, color2)
	palette.setColor(QPalette.AlternateBase, color1)
	palette.setColor(QPalette.ToolTipBase, Qt.black)
	palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
	palette.setColor(QPalette.Text, Qt.white)
	palette.setColor(QPalette.Button, color1)
	palette.setColor(QPalette.ButtonText, Qt.white)
	palette.setColor(QPalette.BrightText, Qt.red)
	palette.setColor(QPalette.Link, '#0ccfb9')
	palette.setColor(QPalette.Highlight, '#0ccfb9')
	palette.setColor(QPalette.HighlightedText, Qt.black)
	palette.setColor(QPalette.Disabled, QPalette.Base, color4)
	palette.setColor(QPalette.Disabled, QPalette.Text, color3)
	palette.setColor(QPalette.Disabled, QPalette.Button, QColor(33, 36, 41))
	palette.setColor(QPalette.Disabled, QPalette.ButtonText, color3)
	palette.setColor(QPalette.Disabled, QPalette.Window, color4)
	palette.setColor(QPalette.Disabled, QPalette.WindowText, color3)
	return palette