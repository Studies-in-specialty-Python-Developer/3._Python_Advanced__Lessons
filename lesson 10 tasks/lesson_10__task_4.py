""" Урок 10, завдання 4
Витягти всі дані про книги (назва, ціна тощо) з сайту
«https://alfavit.eu/index.php?route=product/category&path=_8» та зберегти у БД, де передбачити
можливість зберігати ціну у €, $ та ₴.
"""

import sqlite3
import sys
import traceback
import requests
from bs4 import BeautifulSoup


def database_manipulation(func, arg):
    sqlite_connection = None
    result = None
    try:
        sqlite_connection = sqlite3.connect('lesson_10__task_4_books.sqlite')
        cursor = sqlite_connection.cursor()
        full_arg = [sqlite_connection, cursor]
        full_arg.extend(arg)
        result = func(full_arg)
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
        return result


def create_table(args):
    sqlite_create_table_query = """CREATE TABLE IF NOT EXISTS books (                                
                                title TEXT UNIQUE NOT NULL,
                                price_eur REAL,
                                price_usd REAL,                                
                                price_uah REAL);"""
    args[1].execute(sqlite_create_table_query)
    args[0].commit()


def add_book(args):
    # Предполагается, что таблица книг в базе данных уже создана
    if args[4] == '€':
        field = 'price_eur'
    elif args[4] == '$':
        field = 'price_usd'
    elif args[4] == '₴':
        field = 'price_uah'
    else:
        field = 'price_uah'
    sqlite_add_or_update = f'INSERT INTO books(title, {field}) VALUES ("{args[2]}", {args[3]}) '
    sqlite_add_or_update += f'ON CONFLICT(title) DO UPDATE SET {field}={args[3]};'
    args[1].execute(sqlite_add_or_update)
    args[0].commit()


response = requests.get('https://alfavit.eu/index.php?route=product/category&path=_8', headers={
    'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'})
if response.status_code == 200:
    book_list = dict()
    soup = BeautifulSoup(response.text, 'lxml')
    details = soup.find_all('div', class_='product-details')
    for detail in details:
        title = detail.find('a')
        price_tag = detail.find('span', class_='price-new')
        book_list[title.text] = price_tag.text
else:
    print('Ошибка при получении данных: код', response.status_code)
    exit(0)

# Создание таблицы в базе данных

database_manipulation(create_table, tuple())

# Добавление или обновление данных книги в таблице

for book in book_list:
    title = book
    price, currency = str(book_list[book]).split(' ')
    print(title, price, currency)
    database_manipulation(add_book, (str(title).strip(), price, str(currency).strip()))
