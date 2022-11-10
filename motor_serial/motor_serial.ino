#include <Arduino_PortentaBreakout.h>
#include "mbed.h"
// #include "FATFileSystem.h"
// #include "SDMMCBlockDevice.h"

#define SETPPIN GPIO_1	//Pin 12 
#define DIRPIN GPIO_2	//Pin 11
#define ENAPIN GPIO_3	//Pin 10

// Global variables:
int N_rev_max = 6400;	// Steps per lap - max value (this value has to be the same as the value set in the motor driver)
int N_rev_g = 6400;		// Steps por lap - global value that could change according to the resolution value required by the user
bool dir_g = false;		// Direction (defined as a global variable to change it within a function and call it on other function)
int Pa_g = 0;			// Number of steps used to accelerate
int Tas_g = 0;			// Initial time between steps
int Tai_g = 0;			// Final time between steps
int currentPos_g = 0; 	// Current position (global)

float getSlope(float x1,float y1,float x2,float y2){
	// Helpful function to calculate a slope
	return (y2-y1)/(x2-x1);
}
float getIntercept(float x1,float y1,float m){
	// Helpful function to calculate an intercept
	return y1-m*x1;
}

void forward(int N, bool reverse=false, int Pa=Pa_g, int Tas=Tas_g, int Tai=Tai_g, int N_rev=N_rev_g){
	// Function used to move the motor.
	// N: Number of steps to move.
	// reverse: Direction, false is clockwise, true is counterclockwise
	// Pa, Tas, Tai: Parameters used to perform the motor acceleration	
	// N_rev: Resolution (steps/lap)

	// Variables used to calculate execution times:
	unsigned long init_meas_time = 0;
  	unsigned long stop_meas_time = 0;
  	unsigned long total_meas_time = 0;
  	unsigned long init_time = 0;
  	unsigned long stop_time = 0;
  	unsigned long total_time = 0;
	
	// Variables used to stablish a delay between consecutive motor movements (to prevent malfunctioning)	
	unsigned long previousMicros = 0;  	
	float interval;
	int x = 0;
	int n_step = 0;
	
	// Variables to obtain steps and intercepts for acceleration
	float m1,b1,m2,b2;

	// Variables for the reading and writing process
	int sensorValue = 0;
	float sensorVoltage = 0;
	// Variables used to measure the pin only at 1 out of every X motor movements, according to the required resolution
	int read_cnt = 0;	// Read counter
	int read_mod = N_rev_max/N_rev; // Read divider

	// Set pines for motor movement
	digitalWrite(ENAPIN,LOW);	// Enable pin (low means ready to move)
	digitalWrite(DIRPIN,reverse?LOW:HIGH); 	// Direction pin, set according to required direction
	
	// Calculate acceleration curves:
	if (N<2*Pa){
		m1 = getSlope(0,Tas,Pa,Tai);
		b1 = getIntercept(0,Tas,m1);
		m2 = getSlope((N/2),m1*(N/2)+b1,N,Tas);
		b2 = getIntercept(N,Tas,m2);
	}
	else{
		m1 = getSlope(0,Tas,Pa,Tai);
		b1 = getIntercept(0,Tas,m1);
		m2 = getSlope(N-Pa,Tai,N,Tas);
		b2 = getIntercept(N-Pa,Tai,m2);
	}

	// Movement and reading/writing section:
	init_time = micros();	// Initiate total time measurement (to obtain mean total execution time)
	while(n_step<2*N){
		unsigned long currentMicros = micros();
		
		// Calculate time intervals according to the acceleration curves:
		x = (int)(n_step/2);		
		if (N<2*Pa){
			interval = x<(N/2) ? m1*x + b1 : m2*x + b2;
		}
		else{
			interval = x<Pa ? m1*x + b1 : (x < N-Pa ? Tai : m2*x + b2);			
		}

		// If enough time has passed since the last movement, then move again (used to avoid malfunctioning on some resolutions)		
		if (currentMicros - previousMicros >= interval) {
			previousMicros = currentMicros;	// Update time counter
      		
			// Change pin state from 0 to 1 or 1 to 0 (motor moves on downward edges)
			digitalWrite(SETPPIN,!digitalRead(SETPPIN));
			
			// The motor moves every 1 out of 2 pin changes, so we only have to measure at this times
			if (n_step%2 == 0){
				// The reading has to be done only at 1 out of every read_mod movements, so the required resolution can be 'simulated'
				if (read_cnt%read_mod == 0){
					init_meas_time = micros();	// Initiate time measurement (to obtain mean reading/writing execution time)
					
					// Read pin and send the value through serial port (reading/writing process)
					sensorValue = analogRead(A0);
					sensorVoltage = sensorValue * (3.110/1023.0);
					Serial.print(sensorVoltage);
					Serial.print('-');
        			
					stop_meas_time = micros();	// Stop reading/writing time
					stop_time = micros();		// Stop total time

					total_time = total_time + (stop_time - init_time);   // Add total times 
        			total_meas_time = total_meas_time + (stop_meas_time - init_meas_time);	// Add r/w times

					init_time = micros();	// Re-initiate total time measurement
				}
				read_cnt++;
			}			
			n_step++;
		}
	}  
	// When movement is finished, disable movement pin
	digitalWrite(ENAPIN,HIGH);

	// Calculate mean execution times
  	total_meas_time = total_meas_time/N;
	total_time = total_time/N;

	// Send time data through serial port
	Serial.print(total_meas_time);  
	Serial.print('-');
  	Serial.print(total_time);  
	Serial.print('-');
	return;
}

int calculateStep(String input, int currentPos)
{	
	// Function to calculate how many steps to move and in which direction, according to the received string.

	int steps_to_move = 0;	
	char direction = input[0]; //extract letter
	int N_rx = input.substring(1).toInt(); //extract number

	// The string's first letter indicates the direction.
	// There are 3 cases: 'l' to move counterclockwise, 'r' to move clockwise, 
	// and 'a' to move to an absolute position relative to the initial position.
	switch (direction)
	{
		case 'l': // move to the left, positive, counterclockwise
			steps_to_move = N_rx;
			currentPos = (currentPos + N_rx *(N_rev_max/N_rev_g) ) % N_rev_max;
			dir_g = true;
			break;
		case 'r': // move to the right, negative, clockwise
			steps_to_move = N_rx;
			currentPos = (N_rev_max + currentPos - N_rx *(N_rev_max/N_rev_g) ) % N_rev_max;
			dir_g = false;
			break;
		case 'a': // move to an absolute position (shortest path)
			steps_to_move = N_rx *(N_rev_max/N_rev_g) %N_rev_max - currentPos;
			steps_to_move = steps_to_move / (N_rev_max/N_rev_g);
			if (abs(steps_to_move) <= N_rev_g/2) {
				dir_g = steps_to_move > 0 ? true : false; //left or right?
				steps_to_move = abs(steps_to_move);
			}
			else {
				dir_g = steps_to_move <= 0 ? true : false; //the other way around
				steps_to_move = N_rev_g - abs(steps_to_move);
			}
			currentPos = N_rx *(N_rev_max/N_rev_g) %N_rev_max;
			break;
		default:
			Serial.println("INVALID");
			return -1;
	}	
	
	// Update current position global variable (easier than using array pointers):
	currentPos_g = currentPos;	
	// The steps_to_move calculated value needs to be scaled according to the required 'virtual' resolution:
	steps_to_move = steps_to_move*(N_rev_max/N_rev_g);				

	return steps_to_move;
}

// https://stackoverflow.com/questions/29671455/how-to-split-a-string-using-a-specific-delimiter-in-arduino
String getValue(String data, char separator, int index)
{
	// Function to extract values from strings (used for parameter change string)
  	int found = 0;
  	int strIndex[] = {0, -1};
  	int maxIndex = data.length()-1;

  	for(int i=0; i<=maxIndex && found<=index; i++){
    	if(data.charAt(i)==separator || i==maxIndex){
        	found++;
        	strIndex[0] = strIndex[1]+1;
        	strIndex[1] = (i == maxIndex) ? i+1 : i;
    	}
  	}
  	return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}


void setup() {
	// Set baud rate:
	Serial.begin(9600);

	// Set motor pins mode:
	pinMode(SETPPIN,OUTPUT);
	pinMode(DIRPIN,OUTPUT);
}

void loop() 
{	
	int steps_to_move;	
	String receivedString = "0";
	if (Serial.available() > 0) // Listen for incoming message
	{
		receivedString = Serial.readString();
		receivedString.trim(); // remove \n,\r,\0

		// The received messages can have different forms:
		// If the message is 'p-W-X-Y-Z', then the parameters will be changed according to the 'W-X-Y-Z' values.
		// If the message is 'reset', then the current position is set to be zero.
		// If the message has the form 'xYYY', then the motor will move for 'YYY' steps in 'x' direction.

		// Change parameters:
		if (receivedString[0] == 'p') { //extract letter, 'p' for param changes, p-Nrev-Pa-Tas-Tai
			N_rev_g = getValue(receivedString,'-',1).toInt();
			Pa_g = getValue(receivedString,'-',2).toInt();
			Tas_g = getValue(receivedString,'-',3).toInt();
			Tai_g = getValue(receivedString,'-',4).toInt();
			Serial.println("ack");
			return;
		}

		// Reset position:
		if (receivedString == "reset"){
			currentPos_g = 0;
			Serial.println("ack");
			return;
		}

		// Move motor:
		steps_to_move = calculateStep(receivedString, currentPos_g); // Calculate how many steps to move and get direction from string
		if (steps_to_move == -1){	// If there is an error, do not move
			steps_to_move = 0;
		}
		forward(steps_to_move, dir_g, Pa_g, Tas_g, Tai_g, N_rev_g);	// Move motor

		// These values are sent to the computer through serial port to construct the plots:		
		char real_direction = dir_g ? 'l' : 'r';	// Left or right?

		Serial.print(currentPos_g);
		Serial.print('-');		
		Serial.print(real_direction);
		Serial.print('-');
		Serial.print(steps_to_move);
		Serial.print('-');
		// End message:
		Serial.println(); // \n at the end to let know PC all info has been sent
	}
}

	
