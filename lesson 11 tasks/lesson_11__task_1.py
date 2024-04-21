""" Урок 11, завдання 1
Створити базу даних bookshops, яка містить:
• таблиці:
o books, яка має наступні поля:
➢ первинний ключ (book_id), тип даних INTEGER;
➢ назва книги (title), тип даних TEXT;
➢ жанр (genre), тип даних TEXT;
➢ кількість сторінок (count_page), тип даних INTEGER;
➢ вартість (price), тип даних REAL(у $);
➢ кількість (amount), тип даних INTEGER;
➢ рейтинг (rating), тип даних REAL;
o authors, яка містить наступні поля:
➢ первинний ключ (author_id), тип даних INTEGER;
➢ прізвище (surname), тип даних TEXT;
➢ ім’я (name), тип даних TEXT;
➢ вік (age), тип даних INTEGER;
➢ країна (country), тип даних TEXT;
o auth_book, яка містить наступні поля:
➢ первинний ключ (auth_book _id), тип даних INTEGER;
➢ зовнішній ключ (fk_book_id), тип даних INTEGER;
➢ зовнішній ключ (fk_author_id), тип даних INTEGER;
• у БД повинно бути дані про не менше ніж 250 книжок;
• у БД відтворити наступні вибірки:
o всі автори, вік яких більше 25;
o всі автори, вік яких в діапазоні 35-50 років;
o перші 20 книжок, які мають жанр «детектив»;
o топ-10 книжок у жанрі «Пригоди»;
o результати 31-45, для яких кількість сторінок більше 200
відсортовані за полем назва книги – в лексикографічному
порядку та за кількістю сторінок – за спаданням;
o унікальні країни, автори з яких присутні у БД;
o середня вартість 1 книжки;
o загальна вартість книжок;
o середня вартість 1 книжки у UAH;
o загальна вартість книжок у UAH;
o найдорожча вартість 1 книжки;
o мінімальна вартість 1 книжки;
o кількість книжок у магазині;o кількість унікальних авторів;
• Усі поля повинні містити інформацію. Для швидкого заповнення
таблиць можете скористатися модулями faker та random
"""

import json
import sys
import traceback
import sqlite3
from faker import Faker
from random import randint, choice, random
from collections import Counter

TABLE_ORDER = ('authors', 'books', 'auth_book')
QUANTITY_OF_AUTHORS = 100
QUANTITY_OF_BOOKS = 300
GENRES = ['Fiction', 'Mystery', 'Thriller', 'Romance', 'Science fiction', 'Fantasy', 'Horror', 'Historical fiction',
          'Biography', 'Autobiography', 'Memoir', 'Adventure', 'Young adult', 'Detective', 'Poetry',
          'Drama', 'Comedy', 'Satire', 'Self-help', 'Travel']


def database_manipulation(func, arg):
    sqlite_connection = None
    result = None
    try:
        sqlite_connection = sqlite3.connect('lesson_11__task_1_bookshops.sqlite')
        cursor = sqlite_connection.cursor()
        full_arg = [cursor]
        full_arg.extend(arg)
        result = func(full_arg)
        cursor.close()
        sqlite_connection.commit()
    except sqlite3.Error as error:
        result = None
        print('Exception class: ', error.__class__)
        print('Exception', error.args)
        print('SQLite exception details: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
        sqlite_connection.rollback()
    finally:
        if sqlite_connection:
            sqlite_connection.close()
        return result


def add_new_records(args):
    # args[0] - sqlite3.Cursor object
    # args[1] - SQL query string
    # args[2] - values
    args[0].execute("BEGIN TRANSACTION;")
    args[0].executemany(args[1], args[2])


def execute_script(args):
    # args[0] - sqlite3.Cursor object
    # args[1] - SQL script string
    args[0].execute("BEGIN TRANSACTION;")
    args[0].executescript(args[1])
    return True


def select_data(args):
    # args[0] - sqlite3.Cursor object
    # args[1] - SQL query string
    args[0].execute(args[1], args[2:])
    return args[0].fetchall()


def get_id_list(list_of_tuples: list) -> list:
    return [element[0] for element in list_of_tuples]


with open('lesson_11__task_1_queries.json', 'r') as file:
    queries = json.load(file)

database_manipulation(execute_script, ("PRAGMA foreign_keys = ON;",))

# Создание таблиц в базе данных

sql_script = ''
for table_name in TABLE_ORDER:
    sql_script = ' '.join(queries.get(table_name).get('create'))
    database_manipulation(execute_script, (sql_script,))

# Создание представлений (VIEW) в базе данных

for key, value in queries.get('views').items():
    database_manipulation(execute_script, (' '.join(value),))

# Заполнение таблиц БД тестовыми данными

fake = Faker()

# Создание авторов и запись их в БД
authors_data = []
for _ in range(QUANTITY_OF_AUTHORS):
    author = (fake.last_name(),
              fake.first_name(),
              randint(20, 60),
              fake.country())
    authors_data.append(author)
sql_query = ' '.join(queries.get('authors').get('add'))
database_manipulation(add_new_records, (sql_query, authors_data,))

# Создание книг и запись их в БД
books_data = []
for _ in range(QUANTITY_OF_BOOKS):
    book = (fake.sentence(),
            choice(GENRES),
            randint(50, 500),
            round(random() * 100, 2),
            randint(1, 10),
            round(random(), 4))
    books_data.append(book)
sql_query = ' '.join(queries.get('books').get('add'))
database_manipulation(add_new_records, (sql_query, books_data,))

# Создание таблицы связей между книгами и авторами
author_id_list = get_id_list(database_manipulation(select_data, ("SELECT author_id FROM authors;",)))
book_id_list = get_id_list(database_manipulation(select_data, ("SELECT book_id FROM books;",)))
auth_books = []
for book_id in book_id_list:
    auth_books.append((book_id, choice(author_id_list)))
auth_without_book = set(author_id_list) - set(Counter([item[1] for item in auth_books]).keys())
for auth_id in auth_without_book:
    auth_books.append((choice(book_id_list), auth_id))
sql_query = ' '.join(queries.get('auth_book').get('add'))
database_manipulation(add_new_records, (sql_query, auth_books))
