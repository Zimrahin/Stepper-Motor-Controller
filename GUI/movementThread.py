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
					# angle, direction_char, float_list, mean_time, mean_time_total, values_list = self.right_wdg.unpackData(received_data)
					angle, direction_char, float_list, _, mean_time_total = self.right_wdg.unpackDataBytes(received_data)

					# # SAVE CSV
					# if self.main_wdw.file_name_flag: # mainWindow
					# 	log_time = time.strftime("%H:%M:%S", time.localtime()) #hh:mm:ss
					# 	log_date = time.strftime("%d %B %Y", time.localtime()) #dd monthName year
					# 	# write into CSV file
					# 	log_text = ''
					# 	for n in range(len(values_list)):
					# 		if n < len(values_list) - 1:
					# 			log_text += values_list[n] + ','
					# 		else:
					# 			log_text += values_list[n]

					# 	dir_string = 'clockwise' if direction_char == 'r' else 'counterclockwise'

					# 	header = 	f'{log_date},{log_time},{mean_time}us,{mean_time_total}us,{int(angle)*360./6400}º,{dir_string},{self.right_wdg.azim_params["Nrev"]} step/rev'
					# 	# header = 	log_date + ',' + log_time + ',' + \
					# 	# 			mean_time + 'us,' +  mean_time_total + 'us,' + \
					# 	# 			str(int(angle)*360./6400) + 'º,' + dir_string + ',' + \
					# 	# 			str(self.right_wdg.azim_params['Nrev']) + ' step/rev'
					# 	log_text = f'{header},{log_text}\n'
					# 	# log_text =  header + ',' + log_text + '\n'

					# 	with open(self.main_wdw.file_name,'a') as csvFile:
					# 		csvFile.write(log_text)

					# PLOT
					data_xaxis = self.central_wdg.plot_wdg.updatePlot(float_list, int(angle), direction_char, int(self.right_wdg.azim_params['Nrev']))

					if self.config.dict['debug_print']:
						print(f'len(float_list): {len(float_list)}')
						print(f'angle: {angle}')
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
