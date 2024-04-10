""" Урок 4, завдання 4
Змініть таблицю так, щоби можна було додати не лише витрати, а й доходи.
"""

import sqlite3
import sys
import traceback

sqlite_connection = None
try:
    sqlite_connection = sqlite3.connect('lesson_4__budget.sqlite')
    cursor = sqlite_connection.cursor()
    # Add column "trans_type", 0 - expenses, 1 - incomes
    sql_str = """ALTER TABLE transactions ADD COLUMN trans_type INTEGER;"""
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
