# TO DO LIST
-------
## TO DO

### Reordenar JUEVES
- [ ] Reordenar codigo arduino

### Extras
- [ ] Migrar PyOne dark a PySide2

- [ ] Guardar datos en tarjeta SD

----------------------------------------------------------
### In Progress
### Escritura de CSV/JSON
- [ ] Agregar opción de escribir como JSON


------------------------------------------------------------------------
#### DONE
### Resolución
- [x] Por requerimiento, en la GUI, la resolución ya no debe *espejar* la configuración del driver. El driver debe estar seteado siempre a 6400, y el cambio de resolución en la GUI debe enviar un comando al arduino para **saltarse** una cantidad de steps para minimizar *virtualmente* la resolución.

### Detalles estéticos
- [x] Cambiar avisos de información de pop-ups a mostrarse en la barra de estado (status bar)

# Stepper Motor Controller

Python program with Graphic User Interface that allows communication via serial port with an Arduino Portenta board, which is used to control a stepper motor.

An image of the current state of the GUI is given below
![image](GUI_mockup.png)


# Useful commands
```
pyinstaller --onefile --noconsole --icon logo.ico centralWidget.py
```
