#main
from utils.utils import dynamic_download, download_tripdata
from datetime import date, datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark import SparkContext
import pyspark
import os

def main():

    try:

        # descargar los archivos?
        download_files = input("Download files? (y/n): ").lower() == 'y'

        if download_files:
            # Solicitar parámetros al usuario
            from_date_str = input("Introduce date from (format YYYY-MM-DD): ")
            to_date_str = input("Introduce date to (format YYYY-MM-DD): ")

            # Convertir las fechas ingresadas a objetos date
            from_date = datetime.strptime(from_date_str, "%Y-%m-%d").date()
            to_date = datetime.strptime(to_date_str, "%Y-%m-%d").date()

            dynamic_download(from_date, to_date)

        # Configurar sesión de Spark
        os.environ["PYSPARK_SUBMIT_ARGS"] = "--packages pyspark-shell numpy"

        def create_spark_session(app_name: str = "yellow_app", executor_memory: str = '20g', driver_memory: str = '20g'):
            conf = pyspark.SparkConf().setAll([
                ('spark.executor.memory', executor_memory),
                ('spark.driver.memory', driver_memory)])
            # Required when using GraphFrames
            sc = SparkContext(appName=app_name, master="local[*]", conf=conf)
            spark_session = SparkSession(sc)
            return spark_session 
                
        spark = create_spark_session()
                
        # Leer datos
        raw_data = spark.read.parquet("work_test_app/data/input/*/*.parquet")

        #datos entre las fechas contenidas para tpep_pickup_datetime
        from_date = datetime.strptime(from_date_str, "%Y-%m-%d").date()
        to_date = datetime.strptime(to_date_str, "%Y-%m-%d").date()
        raw_data = raw_data.filter(
            (col("tpep_pickup_datetime") >= from_date) &
            (col("tpep_pickup_datetime") <= to_date)
        )

        #Top 10 viajes por distancia entre las fechas comprendidas
        top_10_data = raw_data.orderBy(col("Trip_distance").desc()).limit(10)
        top_10_data.show()

    #Filtros
        # total_amount
        data_transformed = raw_data.filter(col('total_amount') >= 0)
        data_outliers_total_amount = raw_data.filter(col('total_amount') > 500)

        #trip_distance
        data_outliers_trip_distance = raw_data.filter(col('trip_distance') > 20)

        #...diferentes filtros a aplicar para cada columna

        #eliminamos los outliers
        data_outliers = data_outliers_total_amount.union(data_outliers_trip_distance)
        filtered_data = data_transformed.subtract(data_outliers)

    #Tratamiento de nulos

        #RateCodeID categorica
        filtered_data_filled = filtered_data.fillna(1, subset=['RateCodeID'])

    #validacion
        
        #RatecodeID, airport_fee
        under_pay_data = filtered_data_filled.filter(
                (col('RateCodeID').isin([2, 3, 4])) &
                (col('airport_fee') == 0)
            )
        
        over_pay_data = filtered_data_filled.filter(
                (col('airport_fee') > 0) &
                ~(col('RateCodeID').isin([2, 3, 4]))
            )
        
        #0 =  fare_amount+extra+mta_tax+tolls_amount+improvement_surcharge+congestion_surcharge+airport_fee-total_amount

        silver_data = filtered_data_filled.withColumn(
                'total_fare',
                col('fare_amount') + col('extra') + col('mta_tax') + col('tolls_amount') +
                col('improvement_surcharge') + col('congestion_surcharge') + col('airport_fee') -
                col('total_amount')
            )
        
        # desde aqui podemos ver las diferentes inconsistencias y ver que dicisiones tomar para escoger los datos con los que trabajar en función de la necesidad

    #particionado
        #a la hora de hacer las particiones, podriamos escoger guardarlo en tablas para cada año, estableciendo los indices en función de la necesidad
        silver_data.write.partitionBy('year', 'month').parquet("work_test_app/data/output/")


    except Exception as e:
        print(f"Error en el procesamiento de datos: {e}")

    finally:
        spark.stop()

if __name__ == "__main__":
    main()