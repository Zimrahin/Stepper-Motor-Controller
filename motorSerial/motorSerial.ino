#include <Arduino_PortentaBreakout.h>
#include "mbed.h"
// #include "FATFileSystem.h"
// #include "SDMMCBlockDevice.h"

// Motor 1 (azimuth)
#define SETPIN1 GPIO_1	//Pin 12 
#define DIRPIN1 GPIO_2	//Pin 11
#define ENAPIN1 GPIO_3	//Pin 10
// Motor 2 (elevation)
#define SETPIN2 GPIO_4	//Pin 12
#define DIRPIN2 GPIO_5	//Pin 11
#define ENAPIN2 GPIO_6	//Pin 10

// #define LED_BUILTIN

// Global variables:
int N_rev_max = 6400;	// Steps per rev - max value (this value has to be the same as the value set in the motor driver)
int N_rev_azim_g = 6400;// Steps por rev - global value that could change according to the resolution value required by the user (Azimuth)
int N_rev_elev_g = 6400;// Steps per rev - elevation
bool dir_g = false;		// Direction (defined as a global variable to change it within a function and call it on other function)
int Pa_g_azim = 0;			// Number of steps used to accelerate
int Tas_g_azim = 0;			// Initial time between steps
int Tai_g_azim = 0;			// Final time between steps
int currentPos_azim_g = 0; 	// Current azimuth position (global)
int currentPos_elev_g = 0; 	// Current elevation position (global)

// Default acceleration parameters for elevation (for 200 step/rev)
int Pa_g_elev = 4800;
int Tas_g_elev = 22;
int Tai_g_elev = 12;


float getSlope(float x1,float y1,float x2,float y2){
	// Helpful function to calculate a slope
	return (y2-y1)/(x2-x1);
}
float getIntercept(float x1,float y1,float m){
	// Helpful function to calculate an intercept
	return y1-m*x1;
}

void forward(int N, String motor_type, float* array, int N_measurements, bool reverse=false, int Pa=Pa_g_azim, int Tas=Tas_g_azim, int Tai=Tai_g_azim, int N_rev=N_rev_azim_g, bool print_flag=true) {
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
	int read_counter = 0;	// Read counter
	int read_mod = N_rev_max/N_rev; // Read divider
	int array_counter = 0;

	// Set pines for motor movement
	int enable_pin;
	int dir_pin;
	int set_pin;
	if (motor_type == "motor_azimuth"){
		enable_pin = ENAPIN1;
		dir_pin = DIRPIN1;
		set_pin = SETPIN1;
	}
	else if (motor_type == "motor_elevation"){
		enable_pin = ENAPIN2;
		dir_pin = DIRPIN2;
		set_pin = SETPIN2;
	}	
	digitalWrite(enable_pin,LOW);	// Enable pin (low means ready to move)
	digitalWrite(dir_pin,reverse?LOW:HIGH); 	// Direction pin, set according to required direction
	
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
			digitalWrite(set_pin, !digitalRead(set_pin));
			
			// The motor moves every 1 out of 2 pin changes, so we only have to measure at this times
			if (n_step%2 == 0){
				// The reading has to be done only at 1 out of every read_mod movements, so the required resolution can be 'simulated'
				if (read_counter%read_mod == 0){
					init_meas_time = micros();	// Initiate time measurement (to obtain mean reading/writing execution time)
					
					// Read pin and send the value through serial port (reading/writing process)
					sensorValue = analogRead(A0);
					sensorVoltage = sensorValue * (3.110/1023.0);
					
					if (print_flag){
						// Serial.print(sensorVoltage);
						// Serial.print('-');
						array[array_counter] = sensorVoltage;
						array_counter = array_counter + 1;
					}
        			
					stop_meas_time = micros();	// Stop reading/writing time
					stop_time = micros();		// Stop total time

					total_time = total_time + (stop_time - init_time);   // Add total times 
        			total_meas_time = total_meas_time + (stop_meas_time - init_meas_time);	// Add r/w times

					init_time = micros();	// Re-initiate total time measurement
				}
				read_counter++;
			}			
			n_step++;
		}
	}  
	// When movement is finished, disable movement pin
	digitalWrite(enable_pin,HIGH);

	// Calculate mean execution times
  	total_meas_time = total_meas_time/N;
	total_time = total_time/N;

	// Send time data through serial port
	if (print_flag) {
		Serial.write((char*)array, int(sizeof(float)*N_measurements));
		int int_array[] = {total_meas_time, total_time};
		Serial.write((char*)int_array, int(sizeof(int)*2));
	}

	return;
}

int calculateStep(String input, int currentPos, int N_rev, int* N_meas_ptr, String motor_type="motor_azimuth")
{	
	// Function to calculate how many steps to move and in which direction, according to the received string.

	int steps_to_move = 0;	
	char direction = input[0]; //extract letter
	int N_rx = input.substring(1).toInt(); //extract number

	// The string's first letter indicates the direction.
	// There are 3 cases: 'l' to move counterclockwise, 'r' to move clockwise, 
	// and 'a' to move to an absolute position relative to the initial position.

	if (motor_type == "motor_elevation"){
		if (direction == 'e'){
			direction = 'a';
		}		
		else if (direction == 'u'){
			direction = 'r';
		}
		else if (direction == 'd'){
			direction = 'l';
		}
	}

	switch (direction)
	{
		case 'l': // move to the left, positive, counterclockwise
			steps_to_move = N_rx;
			currentPos = (currentPos + N_rx *(N_rev_max/N_rev) ) % N_rev_max;
			dir_g = true;
			break;
		case 'r': // move to the right, negative, clockwise
			steps_to_move = N_rx;
			currentPos = (N_rev_max + currentPos - N_rx *(N_rev_max/N_rev) ) % N_rev_max;
			dir_g = false;
			break;
		case 'a': // move to an absolute position (shortest path)
			steps_to_move = N_rx *(N_rev_max/N_rev) %N_rev_max - currentPos;
			steps_to_move = steps_to_move / (N_rev_max/N_rev);
			if (abs(steps_to_move) <= N_rev/2) {
				dir_g = steps_to_move > 0 ? true : false; //left or right?
				steps_to_move = abs(steps_to_move);
			}
			else {
				dir_g = steps_to_move <= 0 ? true : false; //the other way around
				steps_to_move = N_rev - abs(steps_to_move);
			}
			currentPos = N_rx *(N_rev_max/N_rev) %N_rev_max;
			break;
		default:
			Serial.println("INVALID");
			return -1;
	}	
	
	// Update current position global variable (easier than using array pointers):
	if (motor_type == "motor_azimuth"){
		currentPos_azim_g = currentPos;	
	}
	else if (motor_type == "motor_elevation"){
		currentPos_elev_g = currentPos;	
	}
	// Assign first a value to malloc
	*N_meas_ptr = steps_to_move;
	// The steps_to_move calculated value needs to be scaled according to the required 'virtual' resolution:
	steps_to_move = steps_to_move*(N_rev_max/N_rev);				

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

void movement(String rcvString, String motor_type="motor_azimuth", bool print_flag=true, int N_rev=N_rev_azim_g, int Pa=Pa_g_azim, int Tas=Tas_g_azim, int Tai=Tai_g_azim){
	int steps_to_move;		
	int currentPos = currentPos_azim_g;
	// variables for malloc()
	int N_measurements; 
	// ESTO NO ES SIEMPRE ASÍ, A80
	float* data_array = NULL;

	if (motor_type == "motor_elevation") {	// Check if the selected motor is the elevation motor, otherwise use default case (azimuth motor)
		N_rev = N_rev_elev_g;	
		currentPos = currentPos_elev_g;
		Pa = Pa_g_elev;
		Tas = Tas_g_elev;
		Tai = Tai_g_elev;
	}
		
	steps_to_move = calculateStep(rcvString, currentPos, N_rev, &N_measurements, motor_type); // Calculate how many steps to move and get direction from string
	if (steps_to_move == -1){	// If there is an error, do not move
		steps_to_move = 0;
	}

	if (print_flag) {
		data_array = (float*) malloc(sizeof(float) * N_measurements);
	}

	forward(steps_to_move, motor_type, data_array, N_measurements, dir_g, Pa, Tas, Tai, N_rev, print_flag);	// Move motor

	// These values are sent to the computer through serial port to make the plots:		
	char real_direction = dir_g ? 'l' : 'r';	// Left or right?

	if (print_flag){
		// Serial.print(String(currentPos_azim_g) + '-' + String(real_direction) + '-' + String(steps_to_move) + '-');
		int int_array[] = {currentPos_azim_g, steps_to_move};
		Serial.write((char*)int_array, int(sizeof(int))*2);
		char char_array[] = {real_direction, '\n'};
		Serial.write((char*)char_array, int(sizeof(char))*2);


		// End message:
		// Serial.println(); // \n at the end to let know PC all info has been sent
	}	
	free(data_array);
	return;	
}

void setup() {
	// Set baud rate:
	Serial.begin(115200);

	// Set motor 1 pins mode:
	pinMode(SETPIN1,OUTPUT);
	pinMode(DIRPIN1,OUTPUT);
	// Set motor 2 pins mode:
	pinMode(SETPIN2,OUTPUT);
	pinMode(DIRPIN2,OUTPUT);


	// Set led pin:
	pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH); 
}

void loop() 
{		
	String receivedString = "0";
	if (Serial.available() > 0) // Wait for incoming message
	{
		receivedString = Serial.readString();
		receivedString.trim(); // remove \n,\r

		// The received messages can have different forms:
		// If the message is 'reset_azim' or 'reset_elev', then the current position is set to be zero.		
		// If the message is 'p-W-X-Y-Z-We-Xe-Ye-Ze', then the parameters will be changed according to the 'W-X-Y-Z' values.		
		// If the message has the form 'xYYY', then the motor will move for 'YYY' steps in 'x' direction.
		// If the message is 'n-aIII-(l/r)FFF-eIII-eFFF', then a routine will be executed in which the azimuth motor moves FFF steps from III position. This is repeated a number times equivalent to a linspace from III to FFF position in elevation according to the elevation resolution set.

		// Set (c)onnection
		if (receivedString[0] == 'c') {
			N_rev_azim_g = getValue(receivedString,'-',1).toInt();
			Pa_g_azim = getValue(receivedString,'-',2).toInt();
			Tas_g_azim = getValue(receivedString,'-',3).toInt();
			Tai_g_azim = getValue(receivedString,'-',4).toInt();
			N_rev_elev_g = getValue(receivedString,'-',5).toInt();
			Pa_g_elev = getValue(receivedString,'-',6).toInt();
			Tas_g_elev = getValue(receivedString,'-',7).toInt();
			Tai_g_elev = getValue(receivedString,'-',8).toInt();
			currentPos_azim_g = 0;
			currentPos_elev_g = 0;
			Serial.println("ack");
			return;
		}

		// Reset position:
		else if (receivedString == "reset_azim"){
			currentPos_azim_g = 0;
			Serial.println("ack");
			return;
		}
		else if (receivedString == "reset_elev"){
			currentPos_elev_g = 0;
			Serial.println("ack");
			return;
		}
		

		// Change (p)arameters:
		else if (receivedString[0] == 'p') { //extract letter, 'p' for param changes, p-NrevAz-Pa-Tas-Tai-NrevEl-PaEl-TasEl-TaiEl
			N_rev_azim_g = getValue(receivedString,'-',1).toInt();
			Pa_g_azim = getValue(receivedString,'-',2).toInt();
			Tas_g_azim = getValue(receivedString,'-',3).toInt();
			Tai_g_azim = getValue(receivedString,'-',4).toInt();
			N_rev_elev_g = getValue(receivedString,'-',5).toInt();
			Pa_g_elev = getValue(receivedString,'-',6).toInt();
			Tas_g_elev = getValue(receivedString,'-',7).toInt();
			Tai_g_elev = getValue(receivedString,'-',8).toInt();
			Serial.println("ack");
			return;
		}

		// Move (a)zimuth motor:
		else if (receivedString[0] == 'a' || receivedString[0] == 'r' || receivedString[0] == 'l' ){
			movement(receivedString);
			return;
		}		

		// Move (e)levation motor:
		else if (receivedString[0] == 'e' || receivedString[0] == 'u' || receivedString[0] == 'd' ){
			movement(receivedString,"motor_elevation",false);
			return;
		}	

		// Routi(n)e:
		else if (receivedString[0] == 'n'){
			// String: n-aIII-(l/r)FFF-eIII-eFFF-N
			// Unpack command:
			String azimString_init = getValue(receivedString,'-',1);
			String azimString_end = getValue(receivedString,'-',2);
			String elevString_init = getValue(receivedString,'-',3);
			String elevString_end = getValue(receivedString,'-',4);	
			int repetitions_per_elevation = getValue(receivedString,'-',5).toInt();
			
			// Calculate steps and linspace for loop:
			int elev_init = elevString_init.substring(1).toInt(); 	//extract number
			int elev_end = elevString_end.substring(1).toInt(); 	//extract number
			int steps = (N_rev_elev_g + (elev_end - elev_init)%N_rev_elev_g)%N_rev_elev_g;
			
			// Initialize motor positions:
			movement(azimString_init, "motor_azimuth", false); // false flag: no serial write
			movement(elevString_init,"motor_elevation", false);

			// Elevation flag for LED blinking
			bool LED_flag = true;

			// Loop:
			String movString_elev;
			int movInt_elev;
			for(int i = 0; i < steps; i++){
				for (int j = 0; j < repetitions_per_elevation; j++) {
					movement(azimString_end);
					movement(azimString_init, "motor_azimuth", false);
				}
				// Temporarily to show change in elevation
				if (LED_flag) digitalWrite(LED_BUILTIN, LOW);
				else digitalWrite(LED_BUILTIN, HIGH); 
				LED_flag = !LED_flag;
							
		
				// movInt_elev = (elev_init + i)%N_rev_elev_g;
				// movString_elev = 'e' + String(movInt_elev);

				// digitalWrite(LED_BUILTIN, LOW);
				// movement(movString_elev,"motor_elevation");
				// Serial.print(movString_elev);
				// digitalWrite(LED_BUILTIN, HIGH); 	

				// Temporarily while having only one motor
				// movement(azimString_init);
			}
			digitalWrite(LED_BUILTIN, HIGH);
			Serial.println("ack"); // Let PC know the routine has ended			
		}
	}
}
	
