import serial   # PySerial
import time    
from matplotlib import pyplot as plt 
import argparse


def csvLogger(opt):
	log_count = 0
	baudrate  = 9600

	# Serial port number and Baud rate
	COMport = 'COM' + input('Enter serial port number: ')
	print('\nPort selected: ', COMport.upper() )
	print('Baud rate: ', baudrate )

	# # Header
	# with open(filename,'w+') as csvFile:
	# 	csvFile.write('No,Date,Time,Step,Voltage\n')
		
	#Open serial port
	serialPort = serial.Serial(COMport,baudrate) 

	time.sleep(3) 	# opening the serial port from Python will reset the Arduino
					
	while True:
		message = input('Write something: ') #r400
		if message == 'end':
			break
		if log_count == 0:
			# File name with current date and time
			filename = time.strftime("%d_%B_%Y_%Hh_%Mm_%Ss.csv", time.localtime())# 20_October_2022_12h_36m_49s
			print(f'\nFile succesfully created: {filename}')
		print('\n')
		serialPort.write(message.encode()) # send '1' to start a routine
		print('\''+message+'\'' + ' sent to Arduino board')
		time.sleep(0.10) # seconds
		receivedString = serialPort.readline()       	# Change to receive mode, Arduino sends \n to terminate
		receivedString = str(receivedString,'utf-8').rstrip() 	# utf8 encoding
		valuesList = receivedString.split('-')[0:-1]	 
		print(valuesList)
		floatList = list(map(float,valuesList))
		plotFunction(floatList)
		
		log_time = time.strftime("%H:%M:%S", time.localtime() ) #hh:mm:ss
		log_date = time.strftime("%d %B %Y", time.localtime() ) #dd monthName year
		
		# write into CSV file
		log_text = ''
		for n in range(len(valuesList)):
			if n < len(valuesList) - 1:
				log_text += valuesList[n] + ','
			else:
				log_text += valuesList[n]
		print(log_text)
		log_text =  str(log_count) + ',' + log_date + ',' + log_time + ',' +  log_text

		with open(filename,'a') as csvFile:
			csvFile.write(log_text)
			
		log_count = log_count + 1 
		# write 'end' to end loop

	serialPort.close()          # Close serial port

def plotFunction(list_in):
	plt.figure(0)
	plt.cla()
	plt.figure(0).patch.set_facecolor('#000000')
	plt.gca().tick_params(axis='x', colors='#ffffff')
	plt.gca().tick_params(axis='y', colors='#ffffff')
	plt.gca().yaxis.label.set_color('#ffffff')
	plt.gca().xaxis.label.set_color('#ffffff')
	#plt.gca().set_aspect('equal')
	#plt.gca().set_ylim(0, height * agentLength / length)
	#plt.gca().set_xlim(0, width * agentLength / length)
	#plt.gca().imshow(cv.cvtColor(frame, cv.COLOR_BGR2RGB), extent=[0, width * agentLength / length, 0, height * agentLength / length])
	plt.plot((range(1,len(list_in)+1)), list_in, color='lime')
	plt.xlabel('N steps')
	plt.ylabel('Voltage')
	plt.figure(0).tight_layout()
	plt.show()

def parse_opt(known=False):
	parser = argparse.ArgumentParser()
	opt = parser.parse_known_args()[0] if known else parser.parse_args()
	return opt

def main(opt):
	csvLogger(opt)

if __name__ == '__main__':
	opt = parse_opt()
	main(opt)