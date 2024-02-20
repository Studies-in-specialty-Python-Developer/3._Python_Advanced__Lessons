""" Урок 4, завдання 1
Зробіть таблицю для підрахунку особистих витрат із такими полями: id, призначення, сума, час.
"""

import sqlite3

sqlite_connection = None
try:
    sqlite_connection = sqlite3.connect('lesson_4__budget.sqlite')
    cursor = sqlite_connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS transactions;')
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            purpose TEXT,
            amount REAL NOT NULL,
            date_time DATETIME NOT NULL
        );
    """)
    sqlite_connection.commit()
    cursor.close()
except sqlite3.Error as error:
    print('SQlite connection error', error)
finally:
    if sqlite_connection:
        sqlite_connection.close()
