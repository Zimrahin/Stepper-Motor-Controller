import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import  Qt
from PyQt5.QtGui import QPalette, QColor

import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import random
import numpy as np


class figCanvas(FigureCanvas):
	def __init__(self, parent=None, width=7.5, height=4, dpi=100):
		self.fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
		self.axes = self.fig.add_subplot(111)
		super(figCanvas, self).__init__(self.fig)

class plotWidget(QWidget):
	def __init__(self, parent=None):
		super(plotWidget, self).__init__(parent)

		# Objects

		# Widgets
		self.canvas_wdg = figCanvas()
		self.toolbar_wdg = NavigationToolbar(self.canvas_wdg)

		# Layout
		layout = QVBoxLayout()
		layout.addWidget(self.canvas_wdg)
		layout.addWidget(self.toolbar_wdg)

		self.setLayout(layout)
	
		self.setMinimumWidth(700)

		self.updatePlot(np.zeros(100), 0, 'l', 100)

	def updatePlot(self, data, angle, direction_char, N_rev):
		scale_factor = 360./N_rev
		self.canvas_wdg.axes.cla()
		if direction_char == 'l': # positive
			self.canvas_wdg.axes.plot( np.linspace((angle+1-len(data))*scale_factor, (angle+1)*scale_factor, len(data)) , data, color='lime')
		else: # negative
			self.canvas_wdg.axes.plot( np.linspace((angle + len(data))*scale_factor, angle*scale_factor, len(data)), data, color='lime')
			self.canvas_wdg.axes.invert_xaxis()

		# self.canvas_wdg.axes.plot(data, color='lime', linewidth=2)

		self.canvas_wdg.axes.set_ylabel('Voltage')
		self.canvas_wdg.axes.yaxis.label.set_color('#ffffff')
		self.canvas_wdg.axes.xaxis.label.set_color('#ffffff')
		self.canvas_wdg.axes.tick_params(axis='x', colors='#ffffff')
		self.canvas_wdg.axes.tick_params(axis='y', colors='#ffffff')
		for spine in self.canvas_wdg.axes.spines.values():
			spine.set_edgecolor('white')
		self.canvas_wdg.axes.spines
		self.canvas_wdg.axes.tick_params(axis='y', colors='#ffffff')
		self.canvas_wdg.fig.set_facecolor('#353535')
		self.canvas_wdg.axes.set_facecolor('#191919')
		self.canvas_wdg.axes.set_xlabel('Degrees')
		self.canvas_wdg.axes.figure.gca().set_ylim(0, 3.2)
		self.canvas_wdg.axes.grid(color = '#353535', linewidth = 1)
		self.canvas_wdg.draw()

def darkMode():
    # Dark Theme
    # Adapted from https://github.com/pyqt/examples/tree/_/src/09%20Qt%20dark%20theme
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    palette.setColor(QPalette.Disabled, QPalette.Base, QColor(49, 49, 49))
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(90, 90, 90))
    palette.setColor(QPalette.Disabled, QPalette.Button, QColor(42, 42, 42))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(90, 90, 90))
    palette.setColor(QPalette.Disabled, QPalette.Window, QColor(49, 49, 49))
    palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(90, 90, 90))
    return palette

if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyle('fusion') 
	palette = darkMode()
	app.setPalette(palette)
	
	main = plotWidget()
	main.show()

	sys.exit(app.exec_())