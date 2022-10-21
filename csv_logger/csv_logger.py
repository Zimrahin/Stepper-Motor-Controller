import serial   # PySerial
import time     

log_count = 0
baudrate  = 9600
loop_flag = True # used to control the While loop querying the Arduino and writing to file

# Serial port number and Baud rate
COMport = 'COM' + input('Enter serial port number: ')
print('\nPort selected: ', COMport.upper() )
print('Baud rate: ', baudrate )

# File name with current date and time
filename = time.strftime("%d_%B_%Y_%Hh_%Mm_%Ss.csv", time.localtime())# 20_October_2022_12h_36m_49s
print(f'\nFile succesfully created: {filename}')

# # Header
# with open(filename,'w+') as csvFile:
# 	csvFile.write('No,Date,Time,Step,Voltage\n')
	
#Open serial port
serialPort = serial.Serial(COMport,baudrate) 

time.sleep(3) 	# opening the serial port from Python will reset the Arduino
	            
while loop_flag:
	message = input('Write something: ')
	if message == 'end':
		break
	print('\n')
	serialPort.write(message.encode()) # send '1' to start a routine
	print('\''+message+'\'' + ' sent to Arduino board')
	time.sleep(0.10) # seconds
	receivedString = serialPort.readline()       	# Change to receive mode, Arduino sends \n to terminate
	receivedString = str(receivedString,'utf-8')	# utf8 encoding
	tempvalueslist = receivedString.split('-')  	 
	#print(tempvalueslist)
	
	log_time = time.strftime("%H:%M:%S", time.localtime() ) #hh:mm:ss
	log_date = time.strftime("%d %B %Y", time.localtime() ) #dd monthName year
	
	# write into CSV file
	log_text = ''
	for n in range(len(tempvalueslist)):
		if n < len(tempvalueslist) - 1:
			log_text += tempvalueslist[n] + ','
		else:
			log_text += tempvalueslist[n]
	print(log_text)
	log_text =  str(log_count) + ',' + log_date + ',' + log_time + ',' +  log_text + '\n'

	with open(filename,'a') as csvFile:
		csvFile.write(log_text)
		
	log_count = log_count + 1 
	# write 'end' to end loop

serialPort.close()          # Close serial port
