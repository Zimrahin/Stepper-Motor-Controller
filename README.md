# TO DO LIST
-------
## TO DO
synthesizer max2871
------------------------------------------------------------------------
### In Progress
---------------------------------------------------------------------
- [ ] Ordenamiento general del código de GUI:
    - [ ] Definir números "hardcoded" en un JSON, que se abra en un config.py como una clase (read only por mientras)
    --------------------------------------------------------------
- [ ] Separar ino file en funciones (según internet basta con separar en .ino mientras estén en la misma carpeta)
- [ ] Arreglar escritura CSV
- [ ] Agregar escritura en CSV para rutina


-------------------------------------------------------------
- [ ] Agregar 'Open File' para plotear
- [ ] Guardar parámetros de rutina en archivos  y agregar "open routine settings"
- [ ] Corregir en Arduino prints ddeben hacerse todos en el mismo lugar. (dentro de la funcion movement), entonces así se podría llamar a otra función con los punteros
- [ ] setear maximo de -30 a 60
- [ ] Agregar exception error box


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
- [x] Escribir informe técnico
- [x] Agregar parametros de aceleración a movimientos de elevación de forma independiente, pero sin posibilidad de cambiarlos desde la GUI
- [x] Solucionar escalamiento con distintas pantallas
*Problema de windows scaling, no vale la pena meterse aquí*

- [x] Solucionar problema de que en la rutina se mueve siempre al camino más corto (a veces se requiere u camino más largo)
- [x] Limitar elevación a -30 , 60 (negativos)
- [x] Agregar posibilidad de moverse en direcciones positivas
- [x] Agregar darkMode como una paleta global que se Importe
------------------------------------------------------------
- [x] Agregar thread a movimientos independientes de motor (r500, a300, etc)
- [x] Cambiar nombre a 'thread' en routine thread (centralWidget)
- [x] Cambiar llamados de parent().parent()... por inicializaciones y nombres especificos
- [x] Corregir que se imprima algo en movimientos de elevación (en la GUI se captura y no se hace nada con la info)
- [x] Arreglar prints (solo debe imprimir en los movimientos l-algo)
- [x] Agregar un 'ack' al final de la rutina en el ardunio para aviarle al python que el proceso termino. El ack triggerea un break en el while, de lo contrario solo se resetea el timeout ocn un continue
- [x] Agregar que e arduino no impprima datos en  estos movimientos, y por lo tanto agregar parametrso aceleracion
- [x] Los prints deben hacerse todos de una vez y al final del movimiento
- [x] Arreglar logica movimiento while true para que el serial no se quede pescado
------------------------------------------------------------------------
### Extras
- [ ] Dejar grafico en decibeles
- [ ] Guardar datos en tarjeta SD
- [ ] Textbox con las frecuencias a utilizar (Ej, [200, 500, 1000             ])
- [ ] botón antena 'sync antennas' (?)

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
