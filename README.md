# Stepper Motor Controller
A simple Graphical User interface made to communicate with a microcontroller via a serial port to control the azimuth and elevation positions of an antenna and plot the power measured at each position.

An image of the current state of the GUI is given below
![image](GUI_mockup.png)

# TO DO LIST
------------------------------------------------------------------
### In Progress
- [x] Agregar escritura en CSV para rutina
- [ ] Agregar lectura de JSON para plot
    - [x] elevation global position is set always from 0 to 6400 in arduino code
-------------------------------------------------------------------

# Useful commands
```
pyinstaller --onefile --noconsole --icon logo.ico mainWindow.py
```
