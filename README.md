# Stepper Motor Controller
A simple Graphical User interface made to communicate with a microcontroller via a serial port to control the azimuth and elevation positions of an antenna and plot the power measured at each position.

An image of the current state of the GUI is given below
![image](GUI_mockup.png)

# TO DO LIST
------------------------------------------------------------------
### In Progress

- [x] Ordenamiento general del código de GUI:
    - [x] mainWindow.py
    - [x] centralWidget.py
    - [x] rightWidget.py
    - [x] connectionWidget.py
    - [x] movementThread.py
    - [x] routineThread.py
    - [x] plotWidget.py

- [ ] JSON file con paleta de colores (usado en palette y en plot)

--------------------------------------------------------------
- [ ] Arreglar escritura CSV
- [ ] Agregar escritura en CSV para rutina
- [ ] Asegurarse que todos los raise Exception funcionen con una ventana pop-up
- [ ] Guardar parámetros de rutina en archivos  y agregar "open routine settings"
- [ ] Separar ino file en funciones (según internet basta con separar en .ino mientras estén en la misma carpeta)
-------------------------------------------------------------
- [ ] Corregir en Arduino prints ddeben hacerse todos en el mismo lugar. (dentro de la funcion movement), entonces así se podría llamar a otra función con los punteros
- [ ] Agregar 'Open File' para plotear
- [ ] Averiguar sobre multithread programming en la portenta (tiene dos núcleos). Esto evitaría tener una pausa después de cada movimiento por el envío de datos
-------------------------------------------------------------------
### Extras
- [ ] Dejar grafico en decibeles
- [ ] Guardar datos en tarjeta SD

### Escritura/Lectura de archivos
- [ ] Agregar opción de escribir como JSON
- [ ] Agregar funcionalidad que permita leer un archivo CSV o JSON y plotear su contenido (en otra pestaña dentro de la misma GUI)



# Useful commands
```
pyinstaller --onefile --noconsole --icon logo.ico centralWidget.py
```
