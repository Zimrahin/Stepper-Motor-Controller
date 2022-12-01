// #include <Arduino_PortentaBreakout.h>
// #include "mbed.h"
#include "SDMMCBlockDevice.h"
#include "FATFileSystem.h"

SDMMCBlockDevice blockDevice;
mbed::FATFileSystem fileSystem("fs");
FILE *myFile;

// Mount File system block
void mountSDCard(){
    int error = fileSystem.mount(&blockDevice);
    if (error){
        Serial.println("Trying to reformat...");
        int formattingError = fileSystem.reformat(&blockDevice);
        if (formattingError) {
            Serial.println("No SD Card found");
            while (1);
        }
    }
}

void setup(){
    Serial.begin(115200);
    delay(1000);

    Serial.println("Mounting SD Card...");
    mountSDCard();
    Serial.println("SD Card mounted.");

    Serial.println("Saving text file to SD card...");
    char myFileName[] = "/fs/test.txt";
    myFile = fopen(myFileName, "a");
    fprintf(myFile,"test\n");
    // fprintf(myFile,"%d,%.2f\n",n_step,sensorVoltage);
    fclose(myFile);

    // delay(100);

    // char ch;
    // // READ
    // myFile = fopen(myFileName, "r");
    // if (myFile) {
    //     Serial.println("content of this file are");
    //     Serial.println(myFileName);
    //     // read from the file until there's nothing else in it:
    //     do {
    //         ch = fgetc(myFile);
    //         Serial.print(ch);
    //     } while (ch != '\n');
    //     Serial.println();
    //     // close the file:
    //     fclose(myFile);
	// } 
    // else {
    //     // if the file didn't open, print an error:
    //     Serial.println("error opening test.txt");
    // }

    fileSystem.unmount();
    Serial.println("Done. You can now remove the SD card.");
}

void loop(){
  //
}
