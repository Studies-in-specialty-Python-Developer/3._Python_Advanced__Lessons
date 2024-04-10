""" Урок 4, завдання 5
Замініть призначення на MCC та використовуйте його для визначення призначення платежу.
"""

import sqlite3
import sys
import traceback

sqlite_connection = None
try:
    sqlite_connection = sqlite3.connect('lesson_4__budget.sqlite')
    cursor = sqlite_connection.cursor()
    sql_str = """ALTER TABLE transactions RENAME COLUMN purpose TO MCC;"""
    cursor.execute(sql_str)
    sqlite_connection.commit()
    cursor.close()
except sqlite3.Error as error:
    print('Exception class: ', error.__class__)
    print('Exception', error.args)
    print('SQLite exception details: ')
    exc_type, exc_value, exc_tb = sys.exc_info()
    print(traceback.format_exception(exc_type, exc_value, exc_tb))
finally:
    if sqlite_connection:
        sqlite_connection.close()
