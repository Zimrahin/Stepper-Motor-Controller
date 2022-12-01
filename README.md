# Stepper Motor Controller
A simple Graphical User interface made to communicate with a microcontroller via a serial port to control the azimuth and elevation positions of an antenna and plot the power measured at each position.

An image of the current state of the GUI is given below
![image](GUI_mockup.png)

# TO DO LIST
------------------------------------------------------------------
### In Progress
- [x] Guardar parámetros de rutina en archivos  y agregar "open routine settings"

- [ ] Documentar código
    - [ ] Class diagram GUI documentation

- [ ] Arreglar escritura CSV
- [ ] Agregar escritura en CSV para rutina


- [ ] Asegurarse que todos los raise Exception funcionen con una ventana pop-up
- [ ] Agregar 'Open File' para plotear (en otra pestaña dentro de la misma GUI)

-------------------------------------------------------------------

# Useful commands
```
pyinstaller --onefile --noconsole --icon logo.ico mainWindow.py
```
