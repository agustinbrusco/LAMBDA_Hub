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

Desde esta screen deberíamos poder ejecutar los archivos `.sh` con protocolos de medición. Por ejemplo, para ejecutar la secuancia de Pocket Pumping en un loop para varios valores de `dTph` puede ejecutarse:
```bash
source loop_pocket_agus_bruno.sh
```
En las primeras lineas de este archivo se define la carpeta donde se guardaran las mediciones ubicada en `~/Soft/ltaDAEMON_main/LAMBDA/images/TRAPS/`. Por convención nombramos a estas carpetas según el día en el que se lanza la medición según `ddMMMyyyy` (ocasionalmente agregando al final del nombre también la temperatura a la que se realizaron).

# Procesamiento de las Mediciones
Los scripts que usamos en general indican el parámetro `NSAMP` > 1, por lo que para visualizar correctamente las imagenes capturadas por una Skipper-CCD es necesario procesarlas. El comando para esto, que debe ejecutarse desde la carpeta dónde se encuentran los archivos `.fits` a procesar es:
```bash
skp -idn <nombre del archivo.fits>
```
Esto genera un archivo `.fits` con el mismo nombre precedido por el prefijo "`proc_`".

Para procesar una carpeta entera podemos usar le script `skp_folder.sh` que se encuentra en `~/Soft/ltaDAEMON_main/LAMBDA/images/TRAPS`. ~~Para esto debemos modificar el archivo `skp_folder.sh` para que contenga el nombre de la carpeta a procesar~~ (NOTA: este archivo desapareció. Encontré uno parecido en carpetas de Santi y dejé una copia en las mediciones de 21NOV o 22NOV aunque funciona distinto y debe colocarse en la carpeta que se quiere procesar en vez de ponerle el nombre) y luego ejecutar:
```bash
source skp_folder.sh
```
Este script también contiene un patrón regex para seleccionar solo los archivos que queremos procesar. En general, para procesar todos los archivos de una carpeta usamos el patrón `*.fits` que selecciona todos los archivos que terminan en `.fits`. Para evitar las "`cleanimg`" que no queremos procesar usamos otros patrones que las excluyen. En el caso del script de Pocket Pumping usamos el patrón `*pocket*.fits` que selecciona todos los archivos que contienen la palabra "`pocket`" en su nombre, o bien `*dTph*.fits` que selecciona todos los archivos que contienen la palabra "`dTph`" en su nombre.

#### Comentario sobre la Edición de Archivos desde la Terminal
Para modificar un archivo desde la terminal podemos usar el editor `nano`. Para abrir un archivo con `nano` ejecutamos:
```bash
nano nombre_del_archivo
```
Esto nos abrirá el archivo en una ventana de `nano` dónde podemos modificarlo. Para guardar los cambios y salir de `nano` ejecutamos `Ctrl+x` y luego `y` para confirmar los cambios. Para salir sin guardar los cambios ejecutamos `Ctrl+x` y luego `n`.

También podemos guardar los cambios a medida que modificamos el archivo con `Ctrl+s`.

## Visualización de las Mediciones
Para visualizar las mediciones usamos el software `ds9`. Para abrir un archivo `.fits` con `ds9` ejecutamos:
```bash
ds9 -mecube <nombre_del_archivo_procesado.fits>
```
O el alias con algún otro parámetro útil:
```bash
dsm <nombre_del_archivo_procesado.fits>
```

## Transferencia de Mediciones
Para transferir las mediciones desde `minilambda` a la computadora local ejecutamos desde la terminal local:
```bash
scp minilambda:~/Soft/ltaDAEMON_main/LAMBDA/images/TRAPS/<ddMMMyyyy_TMPK>/proc_*.fits .
```
Esto copiará todos los archivos que matcheen el patrón "`proc_*.fits`" de la carpeta `<ddMMMyyyy_TMPK>` en `minilambda` a la carpeta local desde la que ejecutamos el comando.