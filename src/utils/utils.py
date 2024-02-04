#utils/utils.py
import os
import requests
from datetime import date
from error_handling.date_handling import handle_date_error


#obtener mes siguiente
def next_date(current_date):

    current_year= current_date.year
    current_month = current_date.month
    day = 28

    next_month = current_month + 1
    next_year = current_year + (next_month // 13)
    next_month = (next_month % 12) or 12  # Ajustar el mes a 12 si es 0

    return date(next_year, next_month, day)

# Obtener fichero del año y mes indicados
def download_tripdata(year, month, destination_folder='work_test_app/data/input'):
    try:
        # URL y la ruta de destino
        base_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_'
        file_format = '.parquet'
        url = f'{base_url}{year}-{month}{file_format}'
        filename = f'yellow_tripdata_{year}-{month}{file_format}'
        destination_path = os.path.join(destination_folder,year, filename)

        # Crea la carpeta si no existe
        os.makedirs(os.path.join(destination_folder, year), exist_ok=True)

        # Descarga el archivo
        response = requests.get(url)
        with open(destination_path, 'wb') as file:
            file.write(response.content)

        return f'downloaded and storaged in: {destination_path}'
    
    except requests.RequestException as req_error:
        print(f"Error al realizar la solicitud HTTP: {req_error}")

    except Exception as e:
        print(f"Error general al descargar para {year}-{month:02d}: {e}")



#Obtener los ficheros desde una fecha inicio a una fecha destino
def dynamic_download(from_date, to_date):
    try:
    # Manejo de errores y reversión de fechas
        from_date, to_date = handle_date_error(from_date, to_date)

        fecha_descarga = from_date

        while fecha_descarga <= to_date:
            year = fecha_descarga.year
            month = fecha_descarga.month

            formatted_month = f"{month:02d}"
            formatted_year = f"{year:04d}"
            #print(f'fecha descarga {fecha_descarga}')
            print(download_tripdata(formatted_year, formatted_month))

            fecha_descarga = next_date(fecha_descarga)

        return f'downloaded data from date {from_date} to date {to_date}'

    except ValueError as e:
        print(f"Error al procesar fechas: {e}. La descarga no se pudo completar.")
