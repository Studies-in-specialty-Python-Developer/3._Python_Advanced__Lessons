""" Урок 4, завдання 3
Створіть агрегатні функції для підрахунку загальної кількості витрат і витрат за місяць. Забезпечте
відповідний інтерфейс користувача.
"""

import sqlite3
import sys
import traceback


def total_expenses(month_number=None):
    sqlite_connection = None
    try:
        sqlite_connection = sqlite3.connect('lesson_4__budget.sqlite')
        cursor = sqlite_connection.cursor()
        sql_str = """SELECT COUNT(*) AS transactions_count, SUM(amount) AS transactions_sum FROM transactions"""
        if month_number:
            sql_str += f" WHERE strftime('%m', date_time) = '{str(month_number).rjust(2, '0')}'"
        sql_str += ';'
        cursor.execute(sql_str)
        result = list(cursor.fetchall()[0])
        cursor.close()
        if result[1] is None:
            result[1] = 0
        return result
    except sqlite3.Error as error:
        print('Exception class: ', error.__class__)
        print('Exception', error.args)
        print('SQLite exception details: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    finally:
        if sqlite_connection:
            sqlite_connection.close()


month = input('Enter the month number (empty line for entire period): ')
count, summ = total_expenses(month)
print(f'Number and amount of expenses for the period: {count} and {summ:.2f}')
