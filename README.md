# LAMBDA_Hub
Autores: Agustín Brusco, Bruno Sivilotti

## Descripción
En este repositorio se encuentra el código generado y los resultados obtenidos durante nuestra participación en diversos proyectos en el Laboratorio Argentino de Mediciones con Bajo umbral de Detección y sus Aplicaciones (LAMBDA). Estos trabajos se dieron en el marco de las materias Laboratorio 6 & 7 de la carrerra de Ciencias Físicas de la Facultad de Ciencias Exactas y Naturales de la Universidad de Buenos Aires.

## Configuración del Entorno
Se recomienda la creación de un entorno virtual. A continuación un ejemplo funcional creado utilizando anaconda:
```bash
conda create --prefix ./lambda_env python=3.11 pip numpy pandas scipy matplotlib seaborn astropy jupyter notebook ipywidgets tqdm
```
(agregar `flake8 black black-jupyter` a la lista de paquetes para homogeneizar el formato es recomendado)

Adicionalmente, la mayoría de los notebooks acceden a una variable de entorno para setear LAMBDA_Hub como la carpeta de trabajo. Para ello se debe crear un archivo local en LAMBDA_Hub/.env con la línea:
```Python
WORKINGDIR="/_Tu_/_Path_/_a_/LAMBDA_Hub"
```