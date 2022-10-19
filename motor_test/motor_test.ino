#include <Arduino_PortentaBreakout.h>
#include "mbed.h"
#include "FATFileSystem.h"
#include "SDMMCBlockDevice.h"

// N: step
// 1.8 deg/N

// Definiciones SD:
SDMMCBlockDevice block_device;
mbed::FATFileSystem fs("fs");

int lap_delay = 1000; //ms
float angle = 720; //deg
int step = floor(angle / 1.8);

// Definicion de pines:
#define SETPPIN GPIO_1  //12 (en esquemático)
#define DIRPIN GPIO_2   //11
#define ENAPIN GPIO_3   //10

// Variables rectas:
int Pa = 1000;           // Cantidad de pasos para acelerar
int Tas = 8000;         // Tiempo inicial entre pasos
int Tai = 5000;			// Tiempo final entre pasos
//const int Tmin = 600; // minimo empírico para que funcione (maxima velocidad), tiempo entre steps

float getSlope(float x1,float y1,float x2,float y2){
  return (y2-y1)/(x2-x1);
}

float getIntercept(float x1,float y1,float m){
  return y1-m*x1;
}

void forward(int N, bool reverse=false){
    // N numero de pasos
    // reverse direccion hacia donde gira, reloj o contrareloj
    unsigned long previousMicros = 0;
    float interval;
    int n_step = 0;
    int x = 0;
    float m1,b1,m2,b2;  
    int sensorValue = 0;
    float sensorVoltage = 0;
    digitalWrite(ENAPIN,LOW);
    digitalWrite(DIRPIN,reverse?LOW:HIGH); 
   
    char myFileName[] = "fs/test2.txt";

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
    myFile = fopen(myFileName, "a");
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
            
            digitalWrite(SETPPIN,!digitalRead(SETPPIN));
            
            sensorValue = analogRead(A0);
            sensorVoltage = sensorValue * (5.0/1023.0);
            n_step++;

            Serial.print(n_step);
            Serial.print(' ');
            Serial.println(sensorVoltage);
            fprintf(myFile,"%d,%.2f\n",n_step,sensorVoltage);
        }
    }
    fclose(myFile);
    digitalWrite(ENAPIN,HIGH);
}

void setup() {
  
    Serial.begin(9600);
    //while (!Serial);

    // pinMode(LEDR,OUTPUT);
    // pinMode(LEDG,OUTPUT);
    // pinMode(LEDB,OUTPUT);
    pinMode(SETPPIN,OUTPUT);
    pinMode(DIRPIN,OUTPUT);

    
    Serial.println("Mounting SDCARD...");
    int err =  fs.mount(&block_device);
    if (err) {
        Serial.println("No SD Card filesystem found, please check SD Card on computer and manually format if needed.");
    }
}

void loop() {
    forward(step);
    delay(lap_delay);
    forward(step,true);
    delay(lap_delay);
}
