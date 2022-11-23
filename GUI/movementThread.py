from PySide2.QtCore import QObject, Signal
import time

class movementThread(QObject):
	finished = Signal()
	progress = Signal(int)

	def __init__(self, right_wdg):
		super().__init__()
		self.right_wdg = right_wdg

	def run(self):
		# READ
		received_string = self.right_wdg.parent().parent().parent().connection_wdg.receiveOnlyCOM()
		angle, direction_char, float_list, mean_time, mean_time_total, values_list = self.right_wdg.unpackData(received_string)

		# SAVE CSV
		if self.right_wdg.parent().parent().parent().parent().file_name_flag: # mainWindow
			log_time = time.strftime("%H:%M:%S", time.localtime()) #hh:mm:ss
			log_date = time.strftime("%d %B %Y", time.localtime()) #dd monthName year
			# write into CSV file
			log_text = ''
			for n in range(len(values_list)):
				if n < len(values_list) - 1:
					log_text += values_list[n] + ','
				else:
					log_text += values_list[n]

			dir_string = 'clockwise' if direction_char == 'r' else 'counterclockwise'
			header = 	log_date + ',' + log_time + ',' + \
						mean_time + 'us,' +  mean_time_total + 'us,' + \
						str(int(angle)*360./6400) + 'º,' + dir_string + ',' + \
						str(self.right_wdg.param_dict['Nrev']) + ' step/rev'
			log_text =  header + ',' + log_text + '\n'

			with open(self.right_wdg.parent().parent().parent().parent().file_name,'a') as csvFile:
				csvFile.write(log_text)

		# PLOT
		data_xaxis = self.right_wdg.parent().parent().parent().plot_wdg.updatePlot(float_list, int(angle), direction_char, int(self.right_wdg.param_dict['Nrev']))		

		# COMPUTE DATA STATISTICS (this section MUST be after updatePlot)
		pp, pa = self.right_wdg.computePeakPower(float_list, data_xaxis)
		mp = self.right_wdg.computeMeanPower(float_list)
		rpm = self.right_wdg.computeRPM(int(mean_time_total))

		self.right_wdg.parent().parent().parent().plot_wdg.pp_label.setText(f'PP = {pp:.2f} V')
		self.right_wdg.parent().parent().parent().plot_wdg.pa_label.setText(f'PA = {pa:.2f}º')
		self.right_wdg.parent().parent().parent().plot_wdg.mp_label.setText(f'MP = {mp:.2f} V')
		self.right_wdg.parent().parent().parent().plot_wdg.rpm_label.setText(f'RPM = {rpm:.1f}')

		self.finished.emit()
