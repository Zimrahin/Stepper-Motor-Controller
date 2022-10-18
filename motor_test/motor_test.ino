#include <Arduino_PortentaBreakout.h>
#include "mbed.h"

// N: step
// 1.8 deg/N

#define SETPPIN GPIO_1 //12
#define DIRPIN GPIO_2 //11
#define ENAPIN GPIO_3 //10

int Pa = 100;
int Tas = 1000;
int Tai = 600;
const int Tmin = 600;

float getSlope(float x1,float y1,float x2,float y2){
  return (y2-y1)/(x2-x1);
}

float getIntercept(float x1,float y1,float m){
  return y1-m*x1;
}

void forward(int N,bool reverse=false){
    //N numero de pasos
    //reverse direccion hacia donde gira, reloj o contrareloj
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
    //myFile = fopen(myFileName, "a");
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
            //fprintf(myFile,"%d,%.2f\n",n_step,sensorVoltage);            
            //Serial.printf("%d,%.2f\n",n_step,sensorVoltage);
        }
    }
    //fclose(myFile);
    digitalWrite(ENAPIN,HIGH);
}

void setup() {
  
    Serial.begin(9600);
    //while (!Serial);

    pinMode(LEDR,OUTPUT);
    pinMode(LEDG,OUTPUT);
    pinMode(LEDB,OUTPUT);
    pinMode(SETPPIN,OUTPUT);
    pinMode(DIRPIN,OUTPUT);
    pinMode(DIRPIN,OUTPUT);       
}

void loop() {
    
    forward(600);
    delay(1000);
    forward(600,true);
    delay(1000);

}
