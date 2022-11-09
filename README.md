# TO DO LIST
-------
## TO DO

### Reordenar JUEVES
- [ ] Reordenar codigo arduino
    - [ ] Cambiar envio de  datos desde arduino a un formato JSON
    - [ ] Ordenar cómo se calcula el eje horizontal para los plot
    - [ ] Debuggear elemento vacío ('') que se envía desde el puerto serial a veces (se envía un elemento más) (código Arduino)

### Extras
- [ ] Implementar shortcut para escritura de datos
    - [ ] enter = move ('s' for now)
    - [ ] any number input must trigger a click in angle spinbox
    - [x] 'a', 'l' and 'r' trigger the radio buttons

- [ ] Migrar PyOne dark a PySide2

- [ ] Guardar datos en tarjeta SD

- [ ] Cambiar avisos de información de pop-ups a mostrarse en la barra de estado (status bar)
----------------------------------------------------------
### In Progress
### Escritura de CSV/JSON
- [ ] Primer 'send' debe comenzar a guardar data en un diccionario o lista
- [ ] Primero se escribe csv apenas se envía el primer dato (igual que en el csv)
- [ ] Se debe agregar widget en QWindow tipo File -> Save as en donde se elija el directorio de destino. De esta manera, una vez se haya finalizado con los experimentos, se guarda el contenido del diccionario/lista creado en un .csv o .json (también debe ser posible elegir esta opción)
- [ ] Usar File > New para comenzar la escritura del CSV!!
- [x] Para el guardado, se debe setear por defecto el nombre que se setea en el csv logger(fecha hora, etc), pero con la opción de cambiarse en la misma ventana pop up
------------------------------------------------------------------------
#### DONE
### Resolución
- [x] Por requerimiento, en la GUI, la resolución ya no debe *espejar* la configuración del driver. El driver debe estar seteado siempre a 6400, y el cambio de resolución en la GUI debe enviar un comando al arduino para **saltarse** una cantidad de steps para minimizar *virtualmente* la resolución.

# Stepper Motor Controller

Python program with Graphic User Interface that allows communication via serial port with an Arduino Portenta board, which is used to control a stepper motor.

An image of the current state of the GUI is given below
![image](GUI_mockup.png)


# Useful commands
```
pyinstaller --onefile --noconsole --icon logo.ico centralWidget.py
```
