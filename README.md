# TO DO LIST
-------
## TO DO


### IMPORTANTE:
- [ ] Revisar que el tiempo promedio por step medido y enviado por la placa sea el correcto, ya que se usa para calcular las RPM
- [ ] Corregir problema que probablemente va a surgir en el argumento del peak power, dado que en cierto caso en el plot, se invierte el xaxis

### Extras
- [ ] Guardar datos en tarjeta SD

### Escritura/Lectura de archivos
- [ ] Agregar opción de escribir como JSON
- [ ] Agregar en csv información de plot : resolución angular y caracter de dirección ('l' o 'r')
- [ ] Agregar funcionalidad que permita leer un archivo CSV o JSON y plotear su contenido (en otra pestaña dentro de la misma GUI)
----------------------------------------------------------
### In Progress
- [x] Agregar tooltips a PP,Pa,MP, RPM
- [ ] Migrar PyOne dark a PySide2
- [ ] Migrar proyecto a pyonedark
------------------------------------------------------------------------
#### DONE


# Stepper Motor Controller

Python program with Graphic User Interface that allows communication via serial port with an Arduino Portenta board, which is used to control a stepper motor.

An image of the current state of the GUI is given below
![image](GUI_mockup.png)


# Useful commands
```
pyinstaller --onefile --noconsole --icon logo.ico centralWidget.py
```
