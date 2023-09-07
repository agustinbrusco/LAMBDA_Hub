# Proyecto de Módulo para la Exposición Controlada de Skipper-CCD
En esta carpeta se encuentran los diseños de piezas que desarrollamos a lo largo de Laboratorio 6 para montar un experimento de exposición controlada en el cubo azul. Para más detalles, puede leerse el informe de Laboratorio 6 en `LAMBDA_Hub/informe_labo6/Informe_labo_6.pdf`.

Los archivos en esta carpeta fueron guardados desde la versión 2020 de SolidWorks. Para compatibilidad con el software de otres laboratoristas, en la carpeta `solid_2016/` se encuentran versiones análogas de algunos archivos en formato válido para la versión 2016 de SolidWorks.

## Descripción de las Piezas Diseñadas
* `shutter_mec_v3.0.SLPDPRT`: Obturador mecánico con encastres y orificios para tornillos. Esta pieza se subdivide en otras dos para facilitar la impresión 3D.
    * `shutter_mec_v3.0_cuerpo.sldprt`: La base del obturador.
    * `shutter_mec_v3.0_tapa.sldprt`: La tapa del obturador.
* `cavidad.SLDPRT`: La base de la cavidad que se encastra al obturador y que tiene orificios para conectar un USB del exterior con un adaptador USB-MiniUSB colocado en el interior de la misma.
* `techo_cavidad.SLDPRT`: El techo encastrable de la cavidad.
* `sosten_laminas.SLDPRT`: Pieza que sostiene las láminas de vidrio y/o film difusor que se colocan entre la cavidad y el obturador.
* `sosten_oled.SLDPRT`: Pieza tipo pilar que encastra en dentro de los orificios en la cavidad y permite sostener una pantalla OLED a la altura del camino óptico central en la pieza.
* `Ensamblaje_todo.SLDASM`: Ensamblaje de todas las piezas mencionadas anteriormente para visualizar el sistema armado y verificar que no haya conflictos en las dimensiones de las piezas.

## Notas Generales del Diseño
* Juego entre piezas: 0,2 mm (0,1 mm para cada lado).
* Tolerancia de impresión: ~0,1 mm (o menos).