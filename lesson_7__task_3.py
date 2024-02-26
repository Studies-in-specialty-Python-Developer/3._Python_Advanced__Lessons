""" Урок 7, завдання 3
Використовуючи модуль sqlite3 та модуль smtplib, реалізуйте реальне додавання користувачів до
бази. Мають бути реалізовані такі функції та класи:
• клас користувача, що містить у собі такі методи: get_full_name (ПІБ з поділом через
пробіл: «Петров Ігор Сергійович»), get_short_name (формату ПІБ: «Петров І. С.»), get_age
(повертає вік користувача, використовуючи поле birthday типу datetime.date); метод
__str__ (повертає ПІБ та дату народження);
• функція реєстрації нового користувача (приймаємо екземпляр нового користувача та
відправляємо email на пошту користувача з листом подяки).
• функція відправлення email з листом подяки.
• функція пошуку користувачів у таблиці users за іменем, прізвищем і поштою.
Протестувати цей функціонал, використовуючи заглушки у місцях надсилання пошти. Під час
штатного запуску програми вона має відправляти повідомлення на вашу реальну поштову
скриньку (необхідно налаштувати SMTP, використовуючи доступи від провайдера вашого emailсервісу).
"""

import sys
import traceback
from email.message import EmailMessage
from datetime import date
import sqlite3
import smtplib
# from unittest.mock import patch

from faker import Faker

DATABASE_NAME = 'lesson_7__task_3.sqlite'


class User:
    first_name: str
    last_name: str
    middle_name: str
    birthday: date
    email: str

    def __init__(self, first_name, last_name, middle_name, birthday, email):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.birthday = birthday
        self.email = email

    def get_full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name])

    def get_short_name(self):
        if self.middle_name:
            return f'{self.last_name} {self.first_name[0]}. {self.middle_name[0]}.'
        return f'{self.last_name} {self.first_name[0]}.'

    def get_age(self):
        age = date.today().year - self.birthday.year - (
                (date.today().month, date.today().day) < (self.birthday.month, self.birthday.day))
        return age

    def __str__(self):
        return f'ФИО: {self.get_full_name()}, д/р: {self.birthday:%d.%m.%Y}'


def database_manipulation(func, arg):
    sqlite_connection = None
    result = None
    try:
        sqlite_connection = sqlite3.connect(DATABASE_NAME)
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
    sqlite_create_table_query = """CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                first_name TEXT NOT NULL,
                                last_name TEXT NOT NULL,
                                middle_name TEXT,                                    
                                birthday DATETIME,
                                email TEXT NOT NULL);"""
    args[1].execute(sqlite_create_table_query)
    args[0].commit()


def thanks_mail(email: str):
    msg = EmailMessage()
    msg.set_content('Thank you very much!')
    msg['Subject'] = 'Thanks'
    msg['From'] = 'python@python.org'
    msg['To'] = email
    # python -m smtpd -n -c DebuggingServer localhost:1025
    sender = smtplib.SMTP(host='localhost', port=1025)
    sender.send_message(msg)
    sender.quit()


def add_new_user(args):
    # Предполагается, что таблица пользователей уже создана
    sqlite_select_with_param = """INSERT or IGNORE INTO users
                                    (first_name, last_name, middle_name, birthday, email)
                                    VALUES (?, ?, ?, ?, ?);"""
    data_tuple = (
        args[2].first_name,
        args[2].last_name,
        args[2].middle_name,
        f'{args[2].birthday:%Y-%m-%d}',
        args[2].email)
    args[1].execute(sqlite_select_with_param, data_tuple)
    args[0].commit()
    print('Добавлен новый пользователь')
    # with patch('__main__.thanks_mail') as mocked_send_email:
    #     mocked_send_email.return_value = 'E-mail sent'
    thanks_mail(args[3].email)


def search_user(args):
    # Предполагается, что таблица пользователей уже создана
    sql_where = ''
    if args[2].get('first_name'):
        sql_where += f' first_name = "{args[2].get("first_name")}" AND'
    if args[2].get('last_name'):
        sql_where += f' last_name = "{args[2].get("last_name")}" AND'
    if args[2].get('email'):
        sql_where += f' email = "{args[2].get("email")}"'
    sql_select_query = "SELECT * FROM users"
    if sql_where:
        sql_select_query = f'SELECT * FROM users WHERE {sql_where}'
        if sql_select_query.endswith(' AND'):
            sql_select_query = sql_select_query[:-4]
    args[1].execute(sql_select_query)
    record = args[1].fetchall()
    result = []
    for row in record:
        result.append(row)
    args[1].close()
    return result


# Чтобы не настраивать реальную почту со своими тонкостями и из соображений приватности для отправки электронного
# письма с благодарностями использовался встроенный SMTP сервер, который предварительно запускается командой
# python -m smtpd -n -c DebuggingServer localhost:1025
# и печатает текст письма в Терминале

# Создание базы пользователей

database_manipulation(create_table, tuple())

# Создание новых пользователей

fake_ua = Faker('uk_UA')
fake_ru = Faker('ru_RU')

user = User(fake_ua.first_name(),
            fake_ua.last_name(),
            fake_ru.middle_name(),
            fake_ru.date_between(start_date='-50y', end_date='-20y'),
            fake_ua.ascii_free_email())
# database_manipulation(add_new_user, (user,))

# Поиск пользователей по составному условию с AND

mask = {'first_name': '', 'last_name': '', 'email': ''}
users_list = database_manipulation(search_user, (mask,))
print(users_list)

# Отправка письма с благодарностями

# with patch('__main__.thanks_mail') as mock_send_email:
#     mock_send_email.return_value = 'E-mail sent'
thanks_mail('serhii74@ukr.net')
