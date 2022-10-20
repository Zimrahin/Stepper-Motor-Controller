//#include <Arduino_PortentaBreakout.h>
//#include "mbed.h"
#include "FATFileSystem.h"
#include "SDMMCBlockDevice.h"

// Definiciones SD:
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
    while (!Serial && millis() < 5000);

    Serial.println("Mounting SD Card...");
    mountSDCard();
    Serial.println("SD Card mounted.");

    Serial.println("Saving text file to SD card...");
    char myFileName[] = "fs/test.txt";
    myFile = fopen(myFileName, "a");
    fprintf(myFile,"test\n");
    fclose(myFile);

    fileSystem.unmount();
    Serial.println("Done. You can now remove the SD card.");
}

void loop(){
  //
}
