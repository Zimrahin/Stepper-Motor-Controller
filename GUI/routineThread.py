from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import QWidget
import sys

class workerThreadPlotUpdate(QObject):
	finished = Signal()
	progress = Signal(int)

	def __init__(self, connection_wdg: QWidget, plot_wdg: QWidget, right_wdg: QWidget, config: object):
		super().__init__()
		self.connection_wdg = connection_wdg
		self.plot_wdg = plot_wdg
		self.right_wdg = right_wdg
		self.config = config

	def run(self):
		#LONG RUNNING TASK
		while(True):
			try:
				received_data = self.connection_wdg.receiveBytesCOM()
				if received_data:
					if received_data == b'ack\r\n':
						break
					# print(received_string)
					angle, direction_char, float_list, _, mean_time_total = self.connection_wdg.unpackDataBytes(received_data)
					# print(float_list)
					if self.config.dict['debug_print']:
						print(len(float_list), direction_char, mean_time_total)
					# PLOT
					data_xaxis = self.plot_wdg.updatePlot(float_list, int(angle), direction_char, int(self.right_wdg.azim_params['Nrev']))		

					# COMPUTE DATA STATISTICS 
					self.plot_wdg.updateDataStatistics(float_list, data_xaxis, mean_time_total)

				else:
					continue
			except:
				(type, value, traceback) = sys.exc_info()
				sys.excepthook(type, value, traceback)
		self.finished.emit()
