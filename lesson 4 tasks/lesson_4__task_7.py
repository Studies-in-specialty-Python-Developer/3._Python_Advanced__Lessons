""" Урок 4, завдання 7
Створіть таблицю для врахування власного бюджету. Напишіть кілька запитів, щоби додати дані
про витрати.
"""

import sqlite3
import datetime
import sys
import traceback


def insert_new_transaction(purpose, amount, date_time, in_out):
    sqlite_connection = None
    try:
        sqlite_connection = sqlite3.connect('lesson_4__budget.sqlite')
        cursor = sqlite_connection.cursor()

        sql_str = """INSERT or IGNORE INTO transactions (MCC, amount, date_time, trans_type) VALUES (?, ?, ?, ?);"""
        data_tuple = (purpose, amount, date_time, in_out)
        cursor.execute(sql_str, data_tuple)
        sqlite_connection.commit()

        sql_str = """SELECT * FROM transactions WHERE date_time = ?"""
        cursor.execute(sql_str, (date_time,))
        record = cursor.fetchone()
        print('   New transaction added:')
        print('ID:', record[0])
        print('Type:', 'expenses' if record[4] == 0 else 'incomes')
        print('MCC code:', record[1])
        print(f'Amount: {record[2]:.2f}')
        print('Added:', record[3], end="\n")
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


expens_income = int(input('Enter the transaction type (0 - expenses, 1 - income): '))
mcc_code = input('Enter MCC code: ')
summa = float(input('Enter amount: '))

insert_new_transaction(mcc_code, summa, datetime.datetime.now(), expens_income)
