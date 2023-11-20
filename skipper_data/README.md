# Notas sobre Medición con Skipper-CCD
Para medir nos conectamos a la computadora `minilambda` que controla el sistema mediante una conexión ssh que es posible solo desde la red del laboratorio. La misma cuenta con tres screens corriendo constantemente:

* `temperatura:` Muestra en pantalla información en vivo sobre la temperatura de la placa en contacto con el Skipper-CCD.
* `configure`: Muestra en pantalla información en vivo sobre la configuración de la placa LTA y las instrucciones que está ejecutando.
* `medicion`: Permite enviar instrucciones a la placa LTA para realizar las mediciones.

Nosotros trabajamos desde el directorio `~/Soft/ltaDAEMON_main/LAMBDA/` donde se encuentran las distintas rutinas como el secuenciador que contiene las instrucciones low-level sobre la configuración del voltaje de los tracks de la CCD permitiendo el movimiento de la carga sobre el mismo y su eventual medición. El directorio `TRAPS` de este repositorio es una copia de una carpeta en `LAMBDA/` donde guardamos las mediciones asociadas a este trabajo. El directorio `scripts_minilambda` contiene los scripts que ejectuados desde `~/Soft/ltaDAEMON_main/LAMBDA/` permiten realizar las mediciones.


# Más en detalle
Para conectarnos a la computadora `minilambda` desde una terminal de linux ejecutamos:
```bash
ssh minilambda
```
Una vez conectados, para ver los screens ejecutamos:
```bash
screen -ls
```
dónde nos aparecerá algo como:
```bash
There are screens on:
        12345.temperatura	(Attached)
        12346.configure	(Attached)
        12347.medicion	(Detached)
3 Sockets in /var/run/screen/S-username.
```
Acá "Attached" significa que el screen está abierto en alguna terminal y "Detached" que no lo está. Para desconectar un screen de otra terminal ejecutamos:
```bash
screen -d nombre_del_screen
```
Para conectarnos a un screen "detacheado" ejecutamos:
```bash
screen -r nombre_del_screen
```
Por último, si queremos crear un nuevo screen ejecutamos:
```bash
screen -S nombre_del_screen
```
Para salir de un screen ejecutamos `Ctrl+a` y luego `d`. Para salir de la conexión ssh ejecutamos `Ctrl+d`.

## Screen temperatura
Este screen muestra en pantalla información en vivo sobre la temperatura de la placa en contacto con el Skipper-CCD. El screen de temperatura en general ya está abierto y printea en pantalla toda la información relacionada a la temperatura cada un par de segundos. Si el screen no está abierto, para abrirlo ejecutamos:
```bash
screen -S temperatura
```
y luego:
```bash
cd ~/Soft/costanera/  # O algo así, preguntar
source activar_temperature.sh
```
Esto abrirá una interfaz de usuario que debemos cerrar con el botón "quit" y luego ejecutar:
```bash
source run_temperature.sh
```
para que comience a printear en pantalla la información de la temperatura. Para salir del screen ejecutamos `Ctrl+a` y luego `d`.

## Screen configure
Este screen muestra en pantalla información en vivo sobre la configuración de la placa LTA y las instrucciones que está ejecutando. El screen de configure en general ya está abierto y printea en pantalla toda la información relacionada a la configuración a medida que la placa recibe comandos y los ejecuta. Si el screen no está abierto, para abrirlo ejecutamos:
```bash
screen -S configure
```
y luego:
```bash
cd ~/Soft/ltaDAEMON_main/LAMBDA/
../configure.exe
```
Esto debería transformar la terminal es un read-only con el log momento a momento d la pataforma. Si necesitamos reiniciar la placa ejecutamos `Ctrl+c` y luego volvemos a correr `../configure.exe`. Para salir del screen ejecutamos `Ctrl+a` y luego `d`.

## Screen medicion
Este screen es simplemente una terminal desde la que correremos los scripts de medición. Este screen debería estar abierto y listo para correr los scripts desde el directorio `~/Soft/ltaDAEMON_main/LAMBDA/`. Si el screen no está abierto, para abrirlo ejecutamos:
```bash
screen -S medicion
```
Y para llegar rápidamente a la carpeta de trabajo ejecutamos:
```bash
lambda
```
el cual es un alias para:
```bash
cd ~/Soft/ltaDAEMON_main/LAMBDA/
```

Desde esta screen deberíamos poder ejecutar los archivos .sh con protocolos de medición. Por ejemplo, para ejecutar la secuancia de Pocket Pumping en un loop para varios valores de `dTph` puede ejecutarse:
```bash
source loop_pocket_agus_bruno.sh
```