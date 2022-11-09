from numpy import unsignedinteger
import serial   # PySerial
import time    
from matplotlib import pyplot as plt, scale
import matplotlib 
matplotlib.use('tkAgg') # solves conflict with pyqt library (use only when running program from terminal)
import argparse
from math import floor
import numpy as np

def csvLogger(opt):
	log_count = 1
	baudrate  = 9600
	serial_timeout = None # seconds

	# Serial port number and Baud rate
	COMport = 'COM' + input('Enter serial port number: ')
	print('\nPort selected: ', COMport.upper() )
	print('Baud rate: ', baudrate )
	
	#Open serial port
	serialPort = serial.Serial(COMport,baudrate = baudrate, timeout=serial_timeout) 

	#Send setup parameters
	N_rev_tx = input('\nEnter number of steps per revolution: ')
	Pa_tx = input('Enter Pa: ')
	Tas_tx = input('Enter Tas: ')
	Tai_tx = input('Enter Tai: ')	
	while(True):
		input_format = input('(d)egrees or (s)teps?: ')
		if input_format != 'd' and input_format != 's':
			continue
		break
	print('\n')
	message = 'p-' + N_rev_tx + '-' + Pa_tx + '-' + Tas_tx + '-' + Tai_tx + '\n'
	serialPort.write(message.encode())
	time.sleep(0.10) # seconds
	ignorado = serialPort.readline()   # para que no se arruine la comunicación serial

	while True:
		message = input('Write something: ') #r400
		if message == 'end':
			break
		if log_count == 1:
			# File name with current date and time
			filename = time.strftime("csv_files/%d_%B_%Y_%Hh_%Mm_%Ss.csv", time.localtime())# 20_October_2022_12h_36m_49s
			print(f'\nFile created successfully: {filename}')
		print('\n')
		# convert angle to step
		if input_format == 'd': # if (d)egrees is selected
			message = angleToStep(message, int(N_rev_tx))
		serialPort.write(message.encode()) #encode message
		print('\''+message+'\'' + ' sent to Arduino board')
		time.sleep(0.10) # seconds
		receivedString = serialPort.readline()       	# Change to receive mode, Arduino sends \n to terminate
		receivedString = str(receivedString,'utf-8').rstrip() 	# utf8 encoding
		valuesList = receivedString.split('-')[0:-1] # there is an empty char at the end 
		print(valuesList) #debug only
		mean_time = valuesList[-5] #microseconds
		mean_time_total = valuesList[-4] #microseconds
		angle = valuesList[-3]
		directionChar = valuesList[-2]
		valuesList = valuesList[0:-5]  #delete last elements
		floatList = list(map(float,valuesList))
		plotFunction(floatList, angle, directionChar, input_format, int(N_rev_tx))
		
		log_time = time.strftime("%H:%M:%S", time.localtime() ) #hh:mm:ss
		log_date = time.strftime("%d %B %Y", time.localtime() ) #dd monthName year
		
		# write into CSV file
		log_text = ''
		for n in range(len(valuesList)):
			if n < len(valuesList) - 1:
				log_text += valuesList[n] + ','
			else:
				log_text += valuesList[n]

		#print(log_text) #debug only
		header = str(log_count) + ',' + log_date + ',' + log_time + ',' + \
					mean_time + 'us,' +  mean_time_total + 'us,' + 'angle ' + angle
		log_text =  header + ',' + log_text + '\n'

		#print(log_text)
		print(header + '\n')

		with open(filename,'a') as csvFile:
			csvFile.write(log_text)
			
		log_count = log_count + 1 
		# write 'end' to end loop

	serialPort.close()          # Close serial port

def plotFunction(list_in, angle, directionChar, input_format, N_rev):
	angle = int(angle)
	# if input_format == 'd':
	# 	angle = angle * 360. / N_rev
	scale_factor = 360./N_rev
	directionFlag = False if directionChar == 'r' else True
	plt.style.use('dark_background')
	plt.figure(0)
	plt.cla()
	plt.gcf().set_size_inches(11, 3)
	plt.figure(0).patch.set_facecolor('#000000')
	plt.gca().tick_params(axis='x', colors='#ffffff')
	plt.gca().tick_params(axis='y', colors='#ffffff')
	plt.gca().yaxis.label.set_color('#ffffff')
	plt.gca().xaxis.label.set_color('#ffffff')
	plt.gca().set_ylim(0, 3.2)
	if directionFlag:
		if input_format == 'd':
			plt.plot( np.linspace((angle+1-len(list_in))*scale_factor, (angle+1)*scale_factor, len(list_in)) , list_in, color='lime')
		else:
			plt.plot( range(angle + 1 - len(list_in), angle + 1) , list_in, color='lime')
	else:
		if input_format == 'd':
			plt.plot(np.linspace((angle + len(list_in))*scale_factor, angle*scale_factor, len(list_in)), list_in, color='lime')
		else:	
			plt.plot( list(range(angle, angle + len(list_in)))[::-1] , list_in, color='lime') 
		plt.gca().invert_xaxis()
	if input_format == 'd':
		plt.xlabel('Degrees')
	else:	
		plt.xlabel('N steps')
	plt.ylabel('Voltage')
	plt.figure(0).tight_layout()
	plt.grid()
	plt.show(block=False) # keep running code

def angleToStep(message_angle, N_max):
	angle = float(message_angle[1:])
	letter = message_angle[0]
	step = str(int(floor(angle * N_max / 360)))
	message_step = letter + step
	return message_step	

def parse_opt(known=False):
	parser = argparse.ArgumentParser()
	opt = parser.parse_known_args()[0] if known else parser.parse_args()
	return opt

def main(opt):
	csvLogger(opt)

if __name__ == '__main__':
	opt = parse_opt()
	main(opt)