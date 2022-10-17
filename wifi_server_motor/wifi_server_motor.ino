#include <WiFi.h>
#include <Arduino_PortentaBreakout.h>
#include "FATFileSystem.h"
#include "mbed.h"

#include "arduino_secrets.h"
#define SETPPIN GPIO_1 //12
#define DIRPIN GPIO_2 //11
#define ENAPIN GPIO_3 //10

///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = SECRET_SSID;    // your network SSID (name)
char pass[] = SECRET_PASS;    // your network password (use for WPA, or use as key for WEP)
int keyIndex = 0;             // your network key Index number (needed only for WEP)

int status = WL_IDLE_STATUS;

WiFiServer server(80);

int Pa = 100;
int Tas = 1000;
int Tai = 600;
const int Tmin = 600;

FILE *myFile;
SDMMCBlockDevice block_device;
mbed::FATFileSystem fs("fs");

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
      fprintf(myFile,"%d,%.2f\n",n_step,sensorVoltage);
    }
  }
  fclose(myFile);
  digitalWrite(ENAPIN,HIGH);
}

void setup() {
  
  Serial.begin(9600);
  while (!Serial);
  
  Serial.println("Access Point Web Server");

  pinMode(LEDR,OUTPUT);
  pinMode(LEDG,OUTPUT);
  pinMode(LEDB,OUTPUT);
  pinMode(SETPPIN,OUTPUT);
  pinMode(DIRPIN,OUTPUT);
  pinMode(DIRPIN,OUTPUT); 

  // check for the WiFi module:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("Communication with WiFi module failed!");
    // don't continue
    while (true);
  }

  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid, pass);

    // wait 3 seconds for connection:
    delay(3000);
  }

  // start the web server on port 80
  server.begin();

  Serial.println("Connected to wifi");

  // you're connected now, so print out the status
  printWifiStatus();
  Serial.println("Mounting SDCARD...");
  int err =  fs.mount(&block_device);
  if (err) {
    // Reformat if we can't mount the filesystem
    // this should only happen on the first boot
    Serial.println("No filesystem found, please check on computer and mually format");
   // err = fs.reformat(&block_device);  // seriously don't want to format good data
  }
  if (err) {
     Serial.println("Error formatting SDCARD ");
     while(1);
  }
}

void loop() {

  WiFiClient client = server.available();   // listen for incoming clients

  if (client) {                             // if you get a client,
    Serial.println("new client");           // print a message out the serial port
    String currentLine = "";                // make a String to hold incoming data from the client
  
    while (client.connected()) {            // loop while the client's connected
     
      if (client.available()) {             // if there's bytes to read from the client,
        char c = client.read();             // read a byte, then
        Serial.write(c);                    // print it out the serial monitor
        if (c == '\n') {                    // if the byte is a newline character

          // if the current line is blank, you got two newline characters in a row.
          // that's the end of the client HTTP request, so send a response:
          if (currentLine.length() == 0) {
            // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
            // and a content-type so the client knows what's coming, then a blank line:
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();

            // the content of the HTTP response follows the header:
            client.print("<html><head>");
            client.print("<style>");
            client.print("* { font-family: sans-serif;}");
            client.print("body { padding: 2em; font-size: 2em; text-align: center;}");            
            client.print("a { -webkit-appearance: button;-moz-appearance: button;appearance: button;text-decoration: none;color: initial; padding: 25px;} #red{color:red;} #green{color:green;} #blue{color:blue;}");
            client.print("</style></head>");
            client.print("<body><h1> MOTOR CONTROLS </h1>");
            client.print("<a href=\"/Hr\">1 LOOP</a> <a href=\"/Lr\">1 LOOP REVERSE</a>");
            client.print("<a href=\"/Hg\">2 LOOP</a> <a href=\"/Lg\">2 LOOP REVERSE</a>");
            client.print("<a href=\"/Hb\">3 LOOP</a> <a href=\"/Lb\">3 LOOP REVERSE</a>");
            client.print("</body></html>");

            // The HTTP response ends with another blank line:
            client.println();
            // break out of the while loop:
            break;
          } else {      // if you got a newline, then clear currentLine:
            currentLine = "";
          }
        } else if (c != '\r') {    // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }

        // Check to see if the client request was "GET /H" or "GET /L":
        if (currentLine.endsWith("GET /Hr")) {
          digitalWrite(LEDR, LOW);               // GET /Hr turns the Red LED on
          forward(200);
        }
        if (currentLine.endsWith("GET /Lr")) {
          digitalWrite(LEDR, HIGH);                // GET /Lr turns the Red LED off
          forward(200,true);
        }
        if (currentLine.endsWith("GET /Hg")){
          digitalWrite(LEDG, LOW);                // GET /Hg turns the Green LED on
          forward(400);
        }
        if (currentLine.endsWith("GET /Lg")){
          digitalWrite(LEDG, HIGH);                // GET /Hg turns the Green LED on
          forward(400,true);
        }
        if (currentLine.endsWith("GET /Hb")){
          digitalWrite(LEDB, LOW);                // GET /Hg turns the Green LED on
          forward(600);
        }
        if (currentLine.endsWith("GET /Lb")){
          digitalWrite(LEDB, HIGH);                // GET /Hg turns the Green LED on
          forward(600,true);
        } 
        
      }
    }
    // close the connection:
    client.stop();
    Serial.println("client disconnected");
  }
  
}

void printRssi() {
  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}

void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  printRssi();
}
