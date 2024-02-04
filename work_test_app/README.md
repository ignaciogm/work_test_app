Como
    ejecuta programa
    ejecuta test
    instala entorno virtual conda venv

como se activa
como se ejecuta el main 
como se ejecutan los test

dependencias

pequeña descripcion del proyecto

# Proyecto de Procesamiento de Datos con PySpark

Este proyecto utiliza PySpark para procesar datos de viajes en taxi de la ciudad de Nueva York. El objetivo es realizar diversas operaciones de limpieza y análisis en los datos y almacenar los resultados en un formato estructurado.

## Requisitos del Proyecto

- Python 3.x
- Apache Spark

## Instalación

1. Clona el repositorio:

    ```bash
    git clone https://github.com/ignaciogm/work_test_app
    ```

2. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. Ejecuta el script `main.py`:

    ```bash
    python main.py
    ```

2. Sigue las instrucciones para ingresar las fechas y decidir si deseas descargar los archivos.


## Estructura del Proyecto

work_test_app/
│   .gitignore
│   problem_description.text
│   README.md
│   requirements.txt
│   resolution.md
│
├───data
│   ├───input
│   └───output
├───src
│   │   main.py
│   ├───error_handling
│   │   │   date_handling.py
│   │   │   __init__.py
│   │
│   └───utils
│       │   pre_analisis_22.txt
│       │   pre_analisis_23.txt
│       │   pre_analysis.py
│       │   utils.py
│
└───tests
        test_date_handling.py
        __init__ .py