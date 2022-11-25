import sys
from PySide2.QtWidgets import QWidget, QVBoxLayout, QApplication, QHBoxLayout, QLabel
from PySide2.QtCore import  Qt

from darkPalette import darkPalette


import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np


class figCanvas(FigureCanvas):
	def __init__(self, parent=None, width=9, height=4, dpi=100):
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
		style_label_string = 'QLabel { color : #ffffff; font: 16pt "Segoe UI"}'
		self.pp_label.setStyleSheet(style_label_string)
		self.pa_label.setStyleSheet(style_label_string)
		self.mp_label.setStyleSheet(style_label_string)
		self.rpm_label.setStyleSheet(style_label_string)
		label_max_height = 28
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

		self.setLayout(vlayout)
	
		self.setMinimumWidth(700)

		self.updatePlot([], 0, 'l', 100)

	def updatePlot(self, data, angle, direction_char, N_rev):
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

		self.canvas_wdg.axes.set_ylabel('Voltage (V)')
		self.canvas_wdg.axes.yaxis.label.set_color('#ffffff')
		self.canvas_wdg.axes.xaxis.label.set_color('#ffffff')
		self.canvas_wdg.axes.tick_params(axis='x', colors='#ffffff')
		self.canvas_wdg.axes.tick_params(axis='y', colors='#ffffff')
		for spine in self.canvas_wdg.axes.spines.values():
			spine.set_edgecolor('#0ccfb9')
		self.canvas_wdg.axes.spines
		self.canvas_wdg.fig.set_facecolor('#2c3136')
		self.canvas_wdg.axes.set_facecolor('#191919')
		self.canvas_wdg.axes.set_xlabel('Degrees (\u00b0)')
		self.canvas_wdg.axes.figure.gca().set_ylim(0, 3.2)
		self.canvas_wdg.axes.grid(color = '#2c3136', linewidth = 1)
		self.canvas_wdg.draw()

		return data_xaxis


if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyle('fusion') 
	palette = darkPalette()
	app.setPalette(palette)
	
	main = plotWidget()
	main.show()

	sys.exit(app.exec_())