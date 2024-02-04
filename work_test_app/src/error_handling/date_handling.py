# error_handling/date_handling.py

from datetime import date

def handle_date_error(start_date, end_date):
    try:

        # Verificar si la fecha de inicio es mayor que la fecha final
        if start_date > end_date:
            raise ValueError("La fecha de inicio no puede ser superior a la fecha final.")

        return start_date, end_date

    except ValueError as e:
        #revertir las fechas
        print(f"Error: {e}. Invertir las fechas.")
        return end_date, start_date
