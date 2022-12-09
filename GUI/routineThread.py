from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import QWidget
import sys

# Worker class for routine movements. 
# Data is plotted in real time for each azimuth movement of data acquisition routine where data is captured.
class workerThreadPlotUpdate(QObject):
	finished = Signal()
	progress = Signal(int)

	def __init__(self, connection_wdg: QWidget, plot_wdg: QWidget, right_wdg: QWidget, config: object, main_wdw: object):
		super().__init__()
		self.connection_wdg = connection_wdg
		self.plot_wdg = plot_wdg
		self.right_wdg = right_wdg
		self.main_wdw = main_wdw
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
					azim_step, direction_char, float_list, mean_time_total, elev_step, n_repetition = self.connection_wdg.unpackDataBytes(received_data)
					# print(float_list)
					if self.config.dict['debug_print']:
						print(len(float_list), direction_char, mean_time_total)

					# SAVE CSV
					if self.main_wdw.file_name_flag: # mainWindow						
						# CALL SAVE_CSV
						rpm = self.plot_wdg.computeRPM(mean_time_total)
						azim_res = self.right_wdg.azim_params["Nrev"]
						elev_res = self.right_wdg.elev_params["Nrev"]
						self.main_wdw.saveCSV(self.main_wdw.file_name, float_list, rpm, azim_step, direction_char, azim_res, elev_step, n_repetition, elev_res)
					

					# PLOT
					data_xaxis = self.plot_wdg.updatePlot(float_list, int(azim_step), direction_char, int(self.right_wdg.azim_params['Nrev']))		

					# COMPUTE DATA STATISTICS 
					self.plot_wdg.updateDataStatistics(float_list, data_xaxis, mean_time_total)

				else:
					continue
			except:
				(type, value, traceback) = sys.exc_info()
				sys.excepthook(type, value, traceback)
		self.finished.emit()
