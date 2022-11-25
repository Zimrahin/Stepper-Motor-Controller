from PySide2.QtCore import Qt
from PySide2.QtGui import QPalette, QColor

def darkPalette(dict: dict):
	# Dark Theme
	palette = QPalette()

	palette.setColor(QPalette.Window, dict['alt_base'])
	palette.setColor(QPalette.WindowText, Qt.white)
	palette.setColor(QPalette.Base, dict['base'])
	palette.setColor(QPalette.AlternateBase, dict['alt_base'])
	palette.setColor(QPalette.ToolTipBase, Qt.black)
	palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
	palette.setColor(QPalette.Text, Qt.white)
	palette.setColor(QPalette.Button, dict['alt_base'])
	palette.setColor(QPalette.ButtonText, Qt.white)
	palette.setColor(QPalette.BrightText, Qt.red)
	palette.setColor(QPalette.Link, dict['highlight'])
	palette.setColor(QPalette.Highlight, dict['highlight'])
	palette.setColor(QPalette.HighlightedText, Qt.black)
	palette.setColor(QPalette.Disabled, QPalette.Base, dict['disabled_base'])
	palette.setColor(QPalette.Disabled, QPalette.Text, dict['disabled_text'])
	palette.setColor(QPalette.Disabled, QPalette.Button, dict["disabled_button"])
	palette.setColor(QPalette.Disabled, QPalette.ButtonText, dict['disabled_text'])
	palette.setColor(QPalette.Disabled, QPalette.Window, dict['disabled_base'])
	palette.setColor(QPalette.Disabled, QPalette.WindowText, dict['disabled_text'])
	return palette