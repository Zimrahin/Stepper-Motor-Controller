# TO DO LIST
-------
## TO DO
synthesizer max2871

### IMPORTANTE:

------------------------------------------------------------------------
### In Progress

- [x] Escribir informe técnico
- [x] Agregar parametros de aceleración a movimientos de elevación de forma independiente, pero sin posibilidad de cambiarlos desde la GUI
- [ ] Agregar escritura en CSV para rutina

------------------------------------------------------------------------
#### DONE
- [x] Dejar tooltips en un método para no desordenar la función principal
- [x] Crear Scroll area para widget derecho
- [x] Cambiar spinbox para que el default se setee automaticamente
- [x] Cambiar tamaño por defecto de las fuentes (con diccionario)
- [x] Agregar otro comando con un widget aparte que diga "start routine" o algo así, que envíe cierto comando que el arduino interprete como (se debe hacer otro case en el loop) que debe tomar las variables globales ya seteadas( resolución polar y de elvación) y hacer una rutina de movimientos desde ej -30 hasta 30 dando X vueltas por cada movimiento de elevación. Para simular esto con un solo motor, se podría hacer un delay al final de un movimiento polar, luego *moverse un step de ida y vuelta (para quedar donde mismo, que represente un movimiento de elevación)* y continuar con la siguiete vuelta
- [x] Corregir radio buttons: los de elevación deben ser independientes a los de azimuth
- [x] Agregar move y reset angle para elevación: deben por mientras imprimir por pantalla un mensaje similar al de azimuth
- [x] Agregar apply global que aplique todos los valores de una vez:
    - [x] Elegir resolución de elevación (la GUI solo debe enviar un comando, que por mientras se puede imprimir, ej: e-6400 (e->elevacion))
    - [x] se deben agregar estos parametros al Arduino
    - [x] se debe corregir el connect (para que tarde menos)
    - [x] Apply y Start deben ir fuera de la scroll bar

- [x] Elegir rango de grados de elevación (Ej: desde: -30º, hasta: 30º)
- [x] Start debe enviar el mensaje con la información de elevación y azimuth elegidas (para elevación se debe transformar lacantidad de veces según la *resolución escogiada* y *la cantidad de grados a moverse*)

- [x] Agregar logica de segundo motor en codigo arduino (DIRPIN2)
- [x] Incorporar funcionalidad de movimientos en elevación (e, u, d), una vez que esté incorporada la funcionalidad de movement con el dirpin seteado
- [x] La rutina debe plotear para cada angulo de elevación
    - Esto no esta funcionando. Es posible que sea porque el plot tarda demasiado, y para entonces ya se tiene la siguiente lectura del puerto serial. Solución: threads? CON THREADS FUNCIONA
- [x] Agregar tooltips para nuevos widgets
- [x] Agregar about y help content
------------------------------------------------------------------------
### Extras
- [ ] Dejar grafico en decibeles
- [ ] Guardar datos en tarjeta SD
- [ ] Textbox con las frecuencias a utilizar (Ej, [200, 500, 1000             ])

### Escritura/Lectura de archivos
- [ ] Agregar opción de escribir como JSON
- [ ] Agregar funcionalidad que permita leer un archivo CSV o JSON y plotear su contenido (en otra pestaña dentro de la misma GUI)

# Stepper Motor Controller

Python program with Graphic User Interface that allows communication via serial port with an Arduino Portenta board, which is used to control a stepper motor.

An image of the current state of the GUI is given below
![image](GUI_mockup.png)


# Useful commands
```
pyinstaller --onefile --noconsole --icon logo.ico centralWidget.py
```
