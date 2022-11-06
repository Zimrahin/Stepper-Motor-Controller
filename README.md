# TO DO LIST

### To do

- [ ] Implementar envío automático de parámetros una vez se logra la conexión (para que sean coherentes los parámatros que se muestran en la GUI con los que tiene guardado el Arduino)
- [ ] Primer 'send' debe comenzar a guardar data en un diccionario o lista
    - [ ] Se debe agregar widget en QWindow tipo File -> Save as en donde se elija el directorio de destino. De esta manera, una vez se haya finalizado con los experimentos, se guarda el contenido del diccionario/lista creado en un .csv o .json (también debe ser posible elegir esta opción)

- [ ] Guardar datos en tarjeta SD

### In Progress

- [ ]   

# Stepper Motor Controller

Python program with Graphic User Interface that allows communication via serial port with an Arduino Portenta board, which is used to control a stepper motor.

An image of the current state of the GUI is given below
![image](GUI_mockup.png)


# Useful commands
```
pyinstaller --onefile --noconsole --icon logo.ico centralWidget.py
```
