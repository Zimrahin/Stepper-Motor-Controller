# Stepper Motor Controller
A simple Graphical User interface made to communicate with a microcontroller via a serial port to control the azimuth and elevation positions of an antenna and plot the power measured at each position.

An image of the current state of the GUI is given below
![image](GUI_mockup.png)

# TO DO LIST
------------------------------------------------------------------
### In Progress
- [ ] Solucionar comunicación serial
    - [ ] Solucionar problema en que al moverse muchas vueltas (más de dos) se pierden datos.

- [ ] Agregar más de un movimiento por elevación
- [ ] Medir tiempo de escritura en sd y comparar con uart
- [ ] Arreglar escritura CSV
- [ ] Agregar escritura en CSV para rutina
- [ ] Documentar código
- [ ] Asegurarse que todos los raise Exception funcionen con una ventana pop-up
- [ ] Guardar parámetros de rutina en archivos  y agregar "open routine settings"

--------------------------------------------------------------
-------------------------------------------------------------
- [ ] Corregir en Arduino prints ddeben hacerse todos en el mismo lugar. (dentro de la funcion movement)
- [ ] Agregar 'Open File' para plotear (en otra pestaña dentro de la misma GUI)
-------------------------------------------------------------------

# Useful commands
```
pyinstaller --onefile --noconsole --icon logo.ico centralWidget.py
```
