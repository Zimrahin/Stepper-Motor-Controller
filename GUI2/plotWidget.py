import sys
from PySide2 import QtGui
from PySide2.QtWidgets import QWidget, QVBoxLayout, QApplication, QHBoxLayout, QLabel
from PySide2.QtCore import  Qt
from PySide2.QtGui import QPalette, QColor, QFont

import matplotlib
matplotlib.use('Qt5Agg')
# matplotlib.rcParams['backend.qt5']='PySide'
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

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
		self.pp_label = QLabel(f'PP = {0.0:.2f} V')
		self.pa_label = QLabel(f'PA = {0.0:.2f}º')
		self.mp_label = QLabel(f'MP = {0.0:.2f} V')
		self.rpm_label = QLabel(f'RPM = {0.0}')
		self.pp_label.setAlignment(Qt.AlignCenter)
		self.pa_label.setAlignment(Qt.AlignCenter)
		self.mp_label.setAlignment(Qt.AlignCenter)
		self.rpm_label.setAlignment(Qt.AlignCenter)
		style_label_string = 'QLabel { color : #FFFFFF; font: 16pt "Segoe UI"}'
		self.pp_label.setStyleSheet(style_label_string)
		self.pa_label.setStyleSheet(style_label_string)
		self.mp_label.setStyleSheet(style_label_string)
		self.rpm_label.setStyleSheet(style_label_string)
		label_max_height = 23
		self.pp_label.setMaximumHeight(label_max_height)
		self.pa_label.setMaximumHeight(label_max_height)
		self.mp_label.setMaximumHeight(label_max_height)
		self.rpm_label.setMaximumHeight(label_max_height)
		self.pp_label.setToolTip('Peak Power')
		self.pa_label.setToolTip('Peak Angle')
		self.mp_label.setToolTip('Mean Power')
		self.rpm_label.setToolTip('Revolutions Per Minute')

		# Layout
		hlayout = QHBoxLayout()
		hlayout.addWidget(self.pp_label)
		hlayout.addWidget(self.pa_label)
		hlayout.addWidget(self.mp_label)
		hlayout.addWidget(self.rpm_label)


		vlayout = QVBoxLayout()
		vlayout.addWidget(self.canvas_wdg)
		vlayout.addLayout(hlayout)
		# layout.addWidget(self.toolbar_wdg)
		# vlayout.addStretch()

		self.setLayout(vlayout)
	
		self.setMinimumWidth(700)

		self.parent().data_xaxis = self.updatePlot([], 0, 'l', 100)

	def updatePlot(self, data, angle, direction_char, N_rev):
		# scale_factor = 360./N_rev
		N_rev_max = 6400
		plot_scale_factor = int(N_rev_max/N_rev)
		angle_scale_factor = 360./N_rev_max
		self.canvas_wdg.axes.cla()
		if direction_char == 'l': # positive
			data_xaxis = np.linspace((angle-len(data) *plot_scale_factor)*angle_scale_factor, angle*angle_scale_factor, len(data))
			self.canvas_wdg.axes.plot( 
				data_xaxis, 
				data, 
				color='#00FFFF')
		else: # negative
			data_xaxis = np.linspace((angle + len(data) *plot_scale_factor)*angle_scale_factor, angle*angle_scale_factor, len(data))
			self.canvas_wdg.axes.plot( 
				data_xaxis, 
				data, 
				color='#00FFFF')
			self.canvas_wdg.axes.invert_xaxis()

		# self.canvas_wdg.axes.plot(data, color='lime', linewidth=2)

		self.canvas_wdg.axes.set_ylabel('Voltage (V)')
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
		self.canvas_wdg.axes.set_xlabel('Degrees (\u00b0)')
		self.canvas_wdg.axes.figure.gca().set_ylim(0, 3.2)
		self.canvas_wdg.axes.grid(color = '#353535', linewidth = 1)
		self.canvas_wdg.draw()

		return data_xaxis

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