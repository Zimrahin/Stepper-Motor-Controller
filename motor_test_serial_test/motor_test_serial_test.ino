#include <Arduino_PortentaBreakout.h>
#include "mbed.h"
// #include "FATFileSystem.h"
// #include "SDMMCBlockDevice.h"

// N: step
// 1.8 deg/N
// Variables globales:

// Definicion de pines:
#define SETPPIN GPIO_1	//12 (en esquemático)
#define DIRPIN GPIO_2	//11
#define ENAPIN GPIO_3	//10

int N_lap_g = 6400;		// steps por vuelta
int Pa_g = 200;			// Cantidad de pasos para acelerar
int Tas_g = 1000;			// Tiempo inicial entre pasos
int Tai_g = 600;			// Tiempo final entre pasos (Tmin = 600)
int currentPos_g = 0; // absolute position "global"
bool param_set_flag = false;

float getSlope(float x1,float y1,float x2,float y2){
	return (y2-y1)/(x2-x1);
}

float getIntercept(float x1,float y1,float m){
	return y1-m*x1;
}

void forward(int N=400, bool reverse=false, int Pa=200, int Tas=1600, int Tai=1000){
	// N numero de pasos
	// reverse direccion hacia donde gira, reloj o contrareloj
	unsigned long previousMicros = 0;
  	unsigned long init_meas_time = 0;
  	unsigned long stop_meas_time = 0;
  	unsigned long total_meas_time = 0;
  	unsigned long init_time = 0;
  	unsigned long stop_time = 0;
  	unsigned long total_time = 0;
	float interval;
	int n_step = 0;
	int x = 0;
	float m1,b1,m2,b2;
	int sensorValue = 0;
	float sensorVoltage = 0;
	digitalWrite(ENAPIN,LOW);
	digitalWrite(DIRPIN,reverse?LOW:HIGH);


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

	init_time = micros();
	while(n_step<2*N){
		unsigned long currentMicros = micros();
		
		x = (int)(n_step/2);		
		if (N<2*Pa){
			interval = x<(N/2) ? m1*x + b1 : m2*x + b2;
		}
		else{
			interval = x<Pa ? m1*x + b1 : (x < N-Pa ? Tai : m2*x + b2);
		}
		if (currentMicros - previousMicros >= interval) {
			previousMicros = currentMicros;

      		init_meas_time = micros();
			digitalWrite(SETPPIN,!digitalRead(SETPPIN));
			
			if (n_step%2 == 0){
				sensorValue = analogRead(A0);
				sensorVoltage = sensorValue * (3.3/1023.0);
				// fprintf(myFile,"%d,%.2f\n",n_step,sensorVoltage);
				Serial.print(sensorVoltage);
				Serial.print('-');
        		stop_meas_time = micros();
				stop_time = micros();
				total_time = total_time + (stop_time - init_time);   
        		total_meas_time = total_meas_time + (stop_meas_time - init_meas_time);       
				init_time = micros();
			}			
			n_step++;
		}
	}  
	digitalWrite(ENAPIN,HIGH);
  	total_meas_time = total_meas_time/N;
	total_time = total_time/N;
	Serial.print(total_meas_time);  
	Serial.print('-');
  	Serial.print(total_time);  
	Serial.print('-');
	// Serial.println(); // \n at the end to let know PC all info has been sent
}

int calculateStep(String input, int currentPos, int N_lap = 6400)
{
	int steps_to_move = 0;
	bool dir_flag = false;
	//N_lap: number of steps equal to one lap
	input.trim(); // remove \n,\r,\0
	char direction = input[0]; //extract letter
	String N_rx_string = input.substring(1); //extract number
	int N_rx = N_rx_string.toInt();
	switch (direction)
	{
		case 'l': // move to the left, positive, counterclockwise
			steps_to_move = N_rx;
			currentPos = (N_lap + currentPos - N_rx)%N_lap;
			dir_flag = true;
			break;
		case 'r': // move to the right, negative, clockwise
			steps_to_move = N_rx;
			currentPos = (currentPos + N_rx)%N_lap;
			dir_flag = false;
			break;
		case 'a': // move to an absolute position (shortest path)
			steps_to_move = N_rx%N_lap - currentPos;
			if (abs(steps_to_move) <= N_lap/2) {
				dir_flag = steps_to_move > 0 ? true : false; //left or right?
				steps_to_move = abs(steps_to_move);
			}
			else {
				dir_flag = steps_to_move <= 0 ? true : false; //the other way around
				steps_to_move = N_lap - abs(steps_to_move);
			}
			currentPos = N_rx%N_lap;
			break;
		default:
			Serial.println("INVALID");
			return -1;
	}
	forward(steps_to_move, dir_flag, Pa_g, Tas_g, Tai_g);
	Serial.print(currentPos);
	Serial.print('-');
	//debug: motor presents non-consistent behaviour
	// no comentar
	char debug_char = dir_flag ? 'l' : 'r';
	Serial.print(debug_char);
	Serial.print('-');
	Serial.print(steps_to_move);
	Serial.print('-');
	return currentPos;
}

// https://stackoverflow.com/questions/29671455/how-to-split-a-string-using-a-specific-delimiter-in-arduino
String getValue(String data, char separator, int index)
{
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
	Serial.begin(9600);
	//while (!Serial);
	pinMode(SETPPIN,OUTPUT);
	pinMode(DIRPIN,OUTPUT);
}

void loop() 
{	
	int resultPos;
	String receivedString = "0";
	if (Serial.available() > 0)
	{
		receivedString = Serial.readString();
		if (!param_set_flag) {
			receivedString.trim(); // remove \n,\r,\0
			N_lap_g = getValue(receivedString,'-',0).toInt();
			Pa_g = getValue(receivedString,'-',1).toInt();
			Tas_g = getValue(receivedString,'-',2).toInt();
			Tai_g = getValue(receivedString,'-',3).toInt();
			param_set_flag = true;
			//Serial.println();
			return;
		}
		resultPos = calculateStep(receivedString, currentPos_g, N_lap_g);
		if (resultPos != -1){
			currentPos_g = resultPos;
		}
		Serial.println(); // \n at the end to let know PC all info has been sent
	}
}

	
