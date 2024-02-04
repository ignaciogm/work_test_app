# Resolution

## Organization

Organizo la estructura de carpetas de los principales componentes que debería incluir la solución. La carpeta de datos de prueba para los test, la carpeta de código, dividida en las etl, validaciones y utilidades extra que pueda necesitar. Y la carpeta de test, donde se irán añadiendo las diferentes pruebas.

1 Analizo los datos: formato, conexion, calidad.
2 Aplicacion python
3 procesamiento con pyspark
4 calidad total_amount

### Formato

Según el formato de los taxis amarillos, nos encontramos con una tabla de hechos con varios campos, del que prestaremos especial atención a Trip_distance(The elapsed trip distance in miles reported by the taximeter), tpep_pickup_datetime(The date and time when the meter was engaged.), tpep_dropoff_datetime(The date and time when the meter was disengaged.) para la solución.

Los datos se obtienen de forma mensual desde el 13/05/2022 y bianual aquellos anteriores a la fecha por lo que procedemos a hacer un análisis de dos ficheros, uno anterior al 13/05/2022 (Enero 2022) y otro posterior (Enero 2023).

### Conexion

Para la descarga, se puede hacer maual o a través de API.El endpoint(https://data.cityofnewyork.us/resource/m6nq-qud6.json), la dcumenación de la API tiene el link roto.  Pero en la página puedo sacar la forma de realizar la descarga. Encuentro que el el link de descarga se puede llamar desde python facilitando el mes y año, de tal manera que puedo usar request para la descarga.

### Calidad

Con los datos del pre_analisis observamos que el número de viajes en el mes un año más tarde, son similares 2,46M, 3M. El número de nulos es 0 para los campos de fecha, el campo de total amount varía en 6$ de media de un año a otro, probablemente debido al incremento de viajes al aeropuerto, con los extras que conlleva. En el campo ya podemos ver en ambos años que el min es saldo negativo, y que el máximo esta por encima de 1K$, asi que profundizamos en la exploración de outliers. También podemos ver que el campo payment_type contiene valores a 0 por lo que habría que ver la calidad de los datos ya que el minimo debería ser 1 como pasa en RateCodeID

## Aplicacion python

Empiezo haciendo pruebas de la descarga de fichero para almacenarlo en la ruta deseada. Tras comprobar que funciona bien, creo una funcion que realice la descarga y me indique la ruta y fichero descargado. Ahora necesito una funcion que con una fecha inicio y fin, me realice la descarga de los meses contenidos en el periodo de tiempo. 

Para saber la fecha siguiente, utilizo la funcion next_date que por simplificarvoy a utilizar siempre el dia 28.

He incluido la gestion de error en download_tripdata y dynamic download. En caso de poner las fechas al revés, invierte las fechas para continuar con el proceso.

Se deberían incluir controles para asegurarse que las fechas que se introducen son correctas y no sean superiores a la fecha actual, asi como la gestion de errores para estas mismas.

Tambien se podrían incluir diferentes test unitarios para simular las respuestas de la llamada http, fechas...

## Procesamiento con pyspark

- eliminar registros con total_amount negativo
- total_amount.
    outliers aquellos por encima de 50$, ya que el 75% estan por debajo de 30$ y el maximo está por encima de 1000$
- trip distance.
    outliers aquellos con mas de 20 millas
- RateCodeID.
    Al ser una columna categórica, en caso de nulo, vamo asustituirlo por 1 = standard rate, aunque sen función del uso que vayamos a hacer de este campo se podrían hacer un tratamiento diferente
-airport_fee.
    comprobar que los datos de airport_fee se incluyen unicamente a aquellos que les han cobrado la tarifa. generar un dataframe con los registro que se les ha cobrado de menos, dataframe con los registros que se les ha cobrado de más

## Almacenamiento

Una vez hayamos definido todo el procesamiento de los datos, procedemos a guardarlo como fiheros parquet particionado por año y mes