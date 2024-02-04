# tests/test_date_handling.py

import unittest
from datetime import date
from error_handling.date_handling import handle_date_error

class TestDateHandling(unittest.TestCase):

    def test_handle_date_error_no_inversion_needed(self):
        start_date = (2023, 1, 10)
        end_date = (2023, 2, 15)

        result_start_date, result_end_date = handle_date_error(start_date, end_date)

        self.assertEqual(result_start_date, date(2023, 1, 10))
        self.assertEqual(result_end_date, date(2023, 2, 15))

    def test_handle_date_error_inversion_needed(self):
        start_date = (2023, 2, 15)
        end_date = (2023, 1, 10)

        result_start_date, result_end_date = handle_date_error(start_date, end_date)

        self.assertEqual(result_start_date, date(2023, 1, 10))
        self.assertEqual(result_end_date, date(2023, 2, 15))

    def test_handle_date_error_invalid_dates(self):
        start_date = (2023, 2, 30)  # Fecha inválida
        end_date = (2023, 1, 10)

        with self.assertRaises(ValueError):
            handle_date_error(start_date, end_date)

if __name__ == '__main__':
    unittest.main()
