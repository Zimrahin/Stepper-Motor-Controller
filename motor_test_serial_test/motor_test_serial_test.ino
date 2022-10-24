#include <Arduino_PortentaBreakout.h>
#include "mbed.h"
// #include "FATFileSystem.h"
// #include "SDMMCBlockDevice.h"

// N: step
// 1.8 deg/N
// Variables rectas:
// int Pa = 200;			// Cantidad de pasos para acelerar
// int Tas = 1600;			// Tiempo inicial entre pasos
// int Tai = 1000;			// Tiempo final entre pasos (Tmin = 600)

// Definicion de pines:
#define SETPPIN GPIO_1	//12 (en esquemático)
#define DIRPIN GPIO_2	//11
#define ENAPIN GPIO_3	//10


int currentPos_g = 0; // absolute position "global"

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

      		init_time = micros();
			digitalWrite(SETPPIN,!digitalRead(SETPPIN));
			
			if (n_step%2 == 0){
				sensorValue = analogRead(A0);
				sensorVoltage = sensorValue * (3.3/1023.0);
				// fprintf(myFile,"%d,%.2f\n",n_step,sensorVoltage);
				Serial.print(sensorVoltage);
				Serial.print('-');
        		stop_time = micros();
        		total_time = total_time + (stop_time - init_time);       
			}
			n_step++;
		}
	}  
	digitalWrite(ENAPIN,HIGH);
  	total_time = total_time/N;
  	Serial.print(total_time);  
	Serial.print('-');
	// Serial.println(); // \n at the end to let know PC all info has been sent
}

int calculateStep(String input, int currentPos)
{
	int steps_to_move = 0;
	bool dir_flag = false;
	int N_lap = 200; //number of steps equal to one lap
	input.trim(); // remove \n,\r,\0
	char direction = input[0];
	String N_rx_string = input.substring(1);
	int N_rx = N_rx_string.toInt();
	switch (direction)
	{
		case 'l':
			steps_to_move = N_rx;
			currentPos = (N_lap + currentPos - N_rx)%N_lap;
			dir_flag = true;
			break;
		case 'r':
			steps_to_move = N_rx;
			currentPos = (currentPos + N_rx)%N_lap;
			dir_flag = false;
			break;
		case 'a':
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
	forward(steps_to_move, dir_flag);
	Serial.print(currentPos);
	Serial.print('-');
	//debug: motor presents non-consistent behaviour
	// char debug_char = dir_flag ? 'l' : 'r';
	// Serial.print(debug_char);
	// Serial.print(steps_to_move);
	// Serial.print('-');
	return currentPos;
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
		resultPos = calculateStep(receivedString, currentPos_g);
		if (resultPos != -1){
			currentPos_g = resultPos;
		}
		Serial.println(); // \n at the end to let know PC all info has been sent
	}
}

	
