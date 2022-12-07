from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import QWidget, QMainWindow
import sys

import time

class movementThread(QObject):
	finished = Signal()
	progress = Signal(int)

	def __init__(self, right_wdg: QWidget, central_wdg: QWidget, main_wdw: QMainWindow):
		super().__init__()
		self.right_wdg = right_wdg
		self.central_wdg = central_wdg
		self.main_wdw = main_wdw
		self.config = self.main_wdw.config


	def run(self):
		while(True):
			try:
				# READ
				received_data = self.central_wdg.connection_wdg.receiveBytesCOM()
				if self.config.dict['debug_print']:
					print(f'len(received_data): {len(received_data)}')
					print(f'last data: {received_data[-18:]}')
				if received_data:
					azim_step, direction_char, float_list, mean_time_total, elev_step, n_repetition = self.central_wdg.connection_wdg.unpackDataBytes(received_data)

					# SAVE CSV
					if self.main_wdw.file_name_flag: # mainWindow						
						# CALL SAVE_CSV
						rpm = self.central_wdg.plot_wdg.computeRPM(mean_time_total)
						azim_res = self.right_wdg.azim_params["Nrev"]
						elev_res = self.right_wdg.elev_params["Nrev"]
						self.main_wdw.saveCSV(self.main_wdw.file_name, float_list, rpm, azim_step, direction_char, azim_res, elev_step, n_repetition, elev_res)						

					# PLOT
					data_xaxis = self.central_wdg.plot_wdg.updatePlot(float_list, int(azim_step), direction_char, int(self.right_wdg.azim_params['Nrev']))

					if self.config.dict['debug_print']:
						print(f'len(float_list): {len(float_list)}')
						print(f'angle: {azim_step}')
						print(f'direction_char: {direction_char}')

					# COMPUTE DATA STATISTICS
					self.central_wdg.plot_wdg.updateDataStatistics(float_list, data_xaxis, mean_time_total)
					
					break
				else:
					continue
			except:
				(type, value, traceback) = sys.exc_info()
				sys.excepthook(type, value, traceback)
		self.finished.emit()
