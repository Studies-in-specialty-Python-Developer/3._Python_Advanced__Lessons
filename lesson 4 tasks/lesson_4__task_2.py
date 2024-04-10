""" Урок 4, завдання 2
Створіть консольний інтерфейс (CLI) на Python для додавання нових записів до бази даних.
"""

import sqlite3
import sys
import traceback
import datetime


def add_record(data_tuple):
    sqlite_connection = None
    try:
        sqlite_connection = sqlite3.connect('lesson_4__budget.sqlite')
        cursor = sqlite_connection.cursor()
        sql_str = """INSERT INTO transactions (purpose, amount, date_time)  VALUES  (?, ?, ?);"""
        cursor.execute(sql_str, data_tuple)
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


purpose = input('Enter purpose: ')
amount = float(input('Enter amount: '))
add_record((purpose, amount, datetime.datetime.now()))
