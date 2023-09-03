# LAMBDA_Hub
Autores: Agustín Brusco, Bruno Sivilotti

## Descripción
En este repositorio se encuentra el código generado y los resultados obtenidos durante nuestra participación en diversos proyectos en el Laboratorio Argentino de Mediciones con Bajo umbral de Detección y sus Aplicaciones (LAMBDA). Estos trabajos se dieron en el marco de las materias Laboratorio 6 & 7 de la carrerra de Ciencias Físicas de la Facultad de Ciencias Exactas y Naturales de la Universidad de Buenos Aires.

## Configuración del Entorno
Se recomienda la creación de un entorno virtual. A continuación un ejemplo funcional creado utilizando anaconda:
```bash
conda create --prefix ./lambda_env python=3.11 pip numpy pandas scipy matplotlib seaborn astropy jupyter notebook ipywidgets
```
(agregar `flake8 black black-jupyter` a la lista de paquetes para homogeneizar el formato es recomendado)