""" Урок 4, завдання 6
Налаштуйте інтеграцію з API свого банку для автоматичного завантаження операцій за картою.
"""

# Personal card transaction data is confidential personal data.
# Instead of this task, a task was made to request bank USD exchange rates.

import datetime
import sqlite3
import requests
import json
import sys
import traceback

DATA_BASE_NAME = 'lesson_4__budget.sqlite'

# Creating a table of USD exchange rates in the database

sqlite_connection = None
try:
    sqlite_connection = sqlite3.connect(DATA_BASE_NAME)
    cursor = sqlite_connection.cursor()
    sqlite_create_table_query = """CREATE TABLE IF NOT EXISTS exchange_rate_tousd (
                                       id INTEGER PRIMARY KEY,
                                       currency_name TEXT,
                                       currency_value REAL,
                                       current_date DATETIME);"""
    cursor.execute(sqlite_create_table_query)
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

# Receiven dollar exchange rates and write them to the database

rate_buy, rate_sell, rate_date = None, None, None
response = requests.get('https://api.monobank.ua/bank/currency')
if response.status_code == 200:
    all_rates = json.loads(response.text)
    for rates in all_rates:
        if rates.get('currencyCodeA') == 840 and rates.get('currencyCodeB') == 980:
            rate_date = datetime.datetime.fromtimestamp(rates['date'])
            rate_buy = rates['rateBuy']
            rate_sell = rates['rateSell']
        break
    # Writing the received USD exchange rate values into the database
    try:
        sqlite_connection = sqlite3.connect(DATA_BASE_NAME)
        cursor = sqlite_connection.cursor()
        sqlite_select_with_param = """INSERT or IGNORE INTO exchange_rate_tousd
                              (currency_name, currency_value, current_date)
                              VALUES (?, ?, ?);"""
        data_tuple = [('UAH - rateBuy', rate_buy, rate_date),
                      ('UAH - rateSell', rate_sell, rate_date)]
        cursor.executemany(sqlite_select_with_param, data_tuple)
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
else:
    print('Error receiving data: code', response.status_code)
