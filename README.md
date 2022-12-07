# Stepper Motor Controller
A simple Graphical User interface made to communicate with a microcontroller via a serial port to control the azimuth and elevation positions of an antenna and plot the power measured at each position.

An image of the current state of the GUI is given below
![image](GUI_mockup.png)

# TO DO LIST
- [ ] Hacer Readme repositorio
- [ ] Comentar todas las funciones de la GUI
------------------------------------------------------------------
- Azimuth elevation control of stepper Motor.
- Azimuth resolution: 6400 step/turn
- Azimuth speed > 100 RPM
- Graphical User Interface can control azimuth range, azimuth speed, elevation range
- A/D conversion and storage of data. Storage time no more than x% of rotation time
- File saving/opening of data acquisition routine settings
- Wireless access of stored data files through LAN/WLAN
- Real time display of acquired data on GUI
- Set angular reference position of stepper motor





# Useful commands
```
pyinstaller --onefile --noconsole --icon logo.ico mainWindow.py
```
