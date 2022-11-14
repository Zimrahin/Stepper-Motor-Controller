# TO DO LIST
-------
## TO DO


### IMPORTANTE:
- [ ] Corregir problema que probablemente va a surgir en el argumento del peak power, dado que en cierto caso en el plot, se invierte el xaxis (se hace con generador de señales)

### Extras
- [ ] Guardar datos en tarjeta SD

### Escritura/Lectura de archivos
- [ ] Agregar opción de escribir como JSON
- [ ] Agregar funcionalidad que permita leer un archivo CSV o JSON y plotear su contenido (en otra pestaña dentro de la misma GUI) 
----------------------------------------------------------
### In Progress
- [ ] Migrar proyecto a pyonedark
------------------------------------------------------------------------
#### DONE
- [x] Revisar que el tiempo promedio por step medido y enviado por la placa sea el correcto, ya que se usa para calcular las RPM
- [x] Agregar tooltips a PP,Pa,MP, RPM
- [x] Migrar PyOne dark a PySide2
- [x] Configurar pyOneDark (title bar, sidebar...)
- [x] Agregar en csv información de plot : resolución angular y caracter de dirección ('l' o 'r')


# Stepper Motor Controller

Python program with Graphic User Interface that allows communication via serial port with an Arduino Portenta board, which is used to control a stepper motor.

An image of the current state of the GUI is given below
![image](GUI_mockup.png)


# Useful commands
```
pyinstaller --onefile --noconsole --icon logo.ico centralWidget.py
```
