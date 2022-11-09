# TO DO LIST

## TO DO
### Escritura de CSV/JSON
- [ ] Primer 'send' debe comenzar a guardar data en un diccionario o lista
    - [ ] Primero se escribe csv apenas se envía el primer dato (igual que en el csv)
    - [ ] Se debe agregar widget en QWindow tipo File -> Save as en donde se elija el directorio de destino. De esta manera, una vez se haya finalizado con los experimentos, se guarda el contenido del diccionario/lista creado en un .csv o .json (también debe ser posible elegir esta opción)

### Reordenar JUEVES
- [ ] Reordenar codigo arduino
    - [ ] Cambiar envio de  datos desde arduino a un formato JSON
    - [ ] Ordenar cómo se calcula el eje horizontal para los plot

### Extras
- [ ] Implementar shortcut para escritura de datos
    - [ ] enter = move ('s' for now)
    - [ ] any number input must trigger a click in angle spinbox
    - [x] 'a', 'l' and 'r' trigger the radio buttons

- [ ] Migrar PyOne dark a PySide2

- [ ] Guardar datos en tarjeta SD

### In Progress

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
