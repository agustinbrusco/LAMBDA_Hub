## Notas sobre Medición con Skipper-CCD
Para medir nos conectamos a la computadora `minilambda` que controla el sistema mediante una conexión ssh que es posible solo desde la red del laboratorio. La misma cuenta con tres screens corriendo constantemente:

* `temp:` Muestra en pantalla información en vivo sobre la temperatura de la placa en contacto con el Skipper-CCD.
* `conf`: Muestra en pantalla información en vivo sobre la configuración de la placa LTA y las instrucciones que está ejecutando.
* `run`: Permite enviar instrucciones a la placa LTA para realizar las mediciones.

Nosotros trabajamos desde el directorio `~/Soft/ltaDAEMON_main/LAMBDA/` donde se encuentran las distintas rutinas como el secuenciador que contiene las instrucciones low-level sobre la configuración del voltaje de los tracks de la CCD permitiendo el movimiento de la carga sobre el mismo y su eventual medición. El directorio `TRAPS` de este repositorio es una copia de una carpeta en `LAMBDA/` donde guardamos las mediciones asociadas a este trabajo. El directorio `scripts_minilambda` contiene los scripts que ejectuados desde `~/Soft/ltaDAEMON_main/LAMBDA/` permiten realizar las mediciones.