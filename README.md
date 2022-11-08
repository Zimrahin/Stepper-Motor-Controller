# TO DO LIST

### To do
- [ ] Primer 'send' debe comenzar a guardar data en un diccionario o lista
    - [ ] Primero se escribe csv apenas se envía el primer dato (igual que en el csv)
    - [ ] Se debe agregar widget en QWindow tipo File -> Save as en donde se elija el directorio de destino. De esta manera, una vez se haya finalizado con los experimentos, se guarda el contenido del diccionario/lista creado en un .csv o .json (también debe ser posible elegir esta opción)

- [ ] Añadir títulos a widgets

- [ ] Guardar datos en tarjeta SD

- [ ] Implementar shortcut para escritura de datos

### In Progress

- [ ] Hover over information (tooltip) for every widget


# Stepper Motor Controller

Python program with Graphic User Interface that allows communication via serial port with an Arduino Portenta board, which is used to control a stepper motor.

An image of the current state of the GUI is given below
![image](GUI_mockup.png)


# Useful commands
```
pyinstaller --onefile --noconsole --icon logo.ico centralWidget.py
```
