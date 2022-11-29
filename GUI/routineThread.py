from PySide2.QtCore import QObject, Signal

class workerThreadPlotUpdate(QObject):
	finished = Signal()
	progress = Signal(int)

	def __init__(self, connection_wdg, plot_wdg, right_wdg, config):
		super().__init__()
		self.connection_wdg = connection_wdg
		self.plot_wdg = plot_wdg
		self.right_wdg = right_wdg
		self.config = config

	def run(self):
		#LONG RUNNING TASK
		while(True):
			received_data = self.connection_wdg.receiveBytesCOM()
			if received_data:
				print(received_data)
				if received_data == b'ack\r\n':
					break
				# print(received_string)
				angle, direction_char, float_list, _, mean_time_total = self.right_wdg.unpackDataBytes(received_data)
				# print(float_list)
				if self.config.dict['debug_print']:
					print(len(float_list), direction_char, mean_time_total)
				#PLOT
				data_xaxis = self.plot_wdg.updatePlot(float_list, int(angle), direction_char, int(self.right_wdg.azim_params['Nrev']))		

				# COMPUTE DATA STATISTICS (this section MUST be after updatePlot)
				pp, pa = self.right_wdg.computePeakPower(float_list, data_xaxis)
				mp = self.right_wdg.computeMeanPower(float_list)
				rpm = self.right_wdg.computeRPM(int(mean_time_total))

				self.plot_wdg.pp_label.setText(f'PP = {pp:.2f} V')
				self.plot_wdg.pa_label.setText(f'PA = {pa:.2f}º')
				self.plot_wdg.mp_label.setText(f'MP = {mp:.2f} V')
				self.plot_wdg.rpm_label.setText(f'RPM = {rpm:.1f}')
			else:
				continue
		self.finished.emit()
