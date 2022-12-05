# Stepper Motor Controller
A simple Graphical User interface made to communicate with a microcontroller via a serial port to control the azimuth and elevation positions of an antenna and plot the power measured at each position.

An image of the current state of the GUI is given below
![image](GUI_mockup.png)

# TO DO LIST
------------------------------------------------------------------
### In Progress
- [ ] Documentar código
    - [ ] Class diagram GUI documentation

- [ ] Agregar escritura en JSON para rutina
- [ ] Agregar lectura de JSON para plot

- [ ] Asegurarse que todos los raise Exception funcionen con una ventana pop-up
-------------------------------------------------------------------

# Useful commands
```
pyinstaller --onefile --noconsole --icon logo.ico mainWindow.py
```
