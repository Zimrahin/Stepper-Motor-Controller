# Stepper Motor Controller
A simple Graphical User interface made to communicate with a microcontroller via a serial port to control the azimuth and elevation positions of an antenna and plot the power measured at each position.

An image of the current state of the GUI is given below
![image](GUI_mockup.png)

# TO DO LIST
------------------------------------------------------------------
### In Progress
- [ ] Guardar parámetros de rutina en archivos  y agregar "open routine settings"

- [x] Agregar más de un movimiento por elevación

- [ ] Arreglar escritura CSV ¿Qué pasa si hago el .exe del código para los valores por defecto de guardado? (i.e. csv_folder)
- [ ] Agregar escritura en CSV para rutina
- [ ] Documentar código
    - [x] Type hinting example:
    ```
    def hello_name(name: str) -> str:
        return(f"Hello {name}")
    ```
    - [ ] Class diagram GUI documentation
- [ ] Asegurarse que todos los raise Exception funcionen con una ventana pop-up
- [ ] Agregar 'Open File' para plotear (en otra pestaña dentro de la misma GUI)

-------------------------------------------------------------
- [ ] Corregir en Arduino prints ddeben hacerse todos en el mismo lugar. (dentro de la funcion movement)
-------------------------------------------------------------------

# Useful commands
```
pyinstaller --onefile --noconsole --icon logo.ico mainWindow.py
```
