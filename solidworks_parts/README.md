# Proyecto de Módulo para la Exposición Controlada de Skipper-CCD

## Descripción de las Piezas Diseñadas
* `shutter_mec_v3.0.SLPDPRT`: Obturador mecánico con encastres y orificios para tornillos. Esta pieza se subdivide en otras dos para facilitar la impresión 3D.
    * `shutter_mec_v3.0_cuerpo.sldprt`: La base del obturador.
    * `shutter_mec_v3.0_tapa.sldprt`: La tapa del obturador.
* `cavidad.SLDPRT`: La base de la cavidad que se encastra al obturador y que tiene orificios para conectar un USB del exterior con un adaptador USB-MiniUSB colocado en el interior de la misma.
* `Ensamblaje_todo.SLDASM`: Ensamblaje de todas las piezas mencionadas anteriormente para visualizar el sistema armado y verificar que no haya conflictos en las dimensiones de las piezas.

## Notas Generales del Diseño
* Juego entre piezas: 0,2 mm (0,1 mm para cada lado).
* Tolerancia de impresión: ~0,1 mm (o menos).