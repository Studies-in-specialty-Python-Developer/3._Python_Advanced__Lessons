""" Урок 11, завдання 3
Спроєктувати БД згідно зі схемою та реалізувати відношення між
сутностями за допомогою SQLite:
4. Таблиця «user» – користувач сервісу. У користувача можуть бути ролі «USER»,
«ADMIN», «SUPER_ADMIN». Ролі мають зберігатися в таблиці «user_role».
«Profile» – профіль користувача, «service» – послуги якими користуються
користувачі, «user_services» – зв'язкова таблиця для «user» та «service», «incident»
– інцидент, що виник, ламання сервісу (тікет, на який має відповісти технічний
спеціаліст).
• Зв'язки між таблицями БД:
• один «user» до одного «profile»;
• один «user» до багатьох «incident»;
• один «user» до одного «user_role»;
• багато «user» до багатьох «service» (кожен користувач може
користуватися безліччю послуг, водночас кожна послуга може мати
багато підписаних користувачів).
• Приймання запитів організувати через консоль. Запити, на які застосунок
має відповідати:
Запит(функції) Опис Доступ
fetch_all_users
Зобразити в консолі список усіх користувачів з усіма залежностями.
«ADMIN», «SUPER_ADMIN»
fetch_all_incidents
fetch_all_active_incidents
Зобразити у консолі список усіх інцидентів і відповідних користувачів без залежностей.
«ADMIN», «SUPER_ADMIN»
fetch _user_by_{id}
Зобразити в консолі користувача за id з усіма залежностями, {id} – параметр «id».
«ADMIN», «SUPER_ADMIN»
add_ user
Створити нового користувача з профілем – у консоль надати статус проведеної операції,
«ADMIN», «SUPER_ADMIN»
виводити допоміжні повідомлення для введення всіх полів користувача та профілю.
update_ user_{id}
Оновити деякі дані поточного користувача за id з профілем – у консоль надати статус проведеної
операції, виводити допоміжні повідомлення для введення всіх полів користувача та профілю,
{id} – параметр «id».
«ADMIN», «SUPER_ADMIN»
del_ user
Видалити користувача за id з усіма залежностями – в консоль надати статус проведеної операції,
{id} – параметр «id».
«ADMIN», «SUPER_ADMIN»
subscribe_service_{id}
Підписатися на послугу, {id} – параметр «id».
«ADMIN», «SUPER_ADMIN», «USER»
unsubscribe_service_{id}
Скасувати підписку на послугу, {id} – параметр «id».
«ADMIN», «SUPER_ADMIN», «USER»
create_incident
Створити інцидент (тікет).
«ADMIN», «SUPER_ADMIN», «USER»
close_incident
Окреслити статус інциденту як завершений.
«ADMIN», «SUPER_ADMIN»
4. Додаткові запити вітаються
"""

import enum
import sys
import traceback
import sqlite3
import json
from pprint import pprint
from faker import Faker
from random import choice, random, randint
from collections import namedtuple

# Порядок создания таблиц в БД, необходим для корректного создания внешних ключей
TABLE_ORDER = ('user_role', 'user', 'profile', 'service', 'user_services', 'incident')

# Количества сущностей в таблицах при автоматической генерации тестовых данных
QUANTITIES = {
    'user': 20,
    'user_role': 3,
    'service': 10,
    'incident': 50,
}

# Кортеж содержит значения констант для выбора роли пользователя: отображаемая строка в меню
RolesValues = namedtuple('RolesValues', ['menu_item'])


class Roles(enum.Enum):
    """ Класс перечисляет роли пользователей базы данных
        роль EXIT добавлена для возможности выхода из программы при автоматическом создании меню выбора ролей
        value в виде кортежа для совместимости со структурой списка команд DMLQueriesValues. Эта структура
        используется при автоматическом создании меню выбора
    """
    USER = RolesValues('USER')
    ADMIN = RolesValues('ADMIN')
    SUPER_ADMIN = RolesValues('SUPER ADMIN')
    EXIT = RolesValues('EXIT')


# Кортеж содержит значения констант для запросов к БД: отображаемая строка в меню, отчет о выполнении запроса,
# допустимые роли пользователей, функция для выполнения запроса.
DMLQueriesValues = namedtuple('DMLQueriesValues', ['menu_item', 'report', 'roles', 'oper_func'])


def select_data(args: tuple):
    """ Формирует запрос на выборку данных из БД
    Структура списка аргументов:
        args[0] - sqlite3.Cursor object
        args[1] - SQL query string
        args[2:] - query parameters (if any)
    Returns:
        list of tuples with fetched data
    """
    args[0].execute(args[1], args[2:])
    return args[0].fetchall()


def execute_script(args: tuple):
    """ Формирует запрос на изменение, добавление, удаление данных из БД
    Структура списка аргументов:
        args[0] - sqlite3.Cursor object
        args[1] - SQL query string
    """
    args[0].execute("BEGIN TRANSACTION;")
    args[0].executescript(args[1])
    return True


class DMLQueries(enum.Enum):
    """ Класс перечисляет список команд для добавления, удаления, выборки, изменения данных в БД
        команда exit добавлена для возможности выхода из программы при автоматическом создании меню выбора команды
    """
    fetch_all_users = DMLQueriesValues('Display a list of all users with all dependencies',
                                       'List of all users with all dependencies:',
                                       [Roles.ADMIN, Roles.SUPER_ADMIN], select_data)
    fetch_user_by_id = DMLQueriesValues('Display user by id with all dependencies',
                                        'User data with ID = 1? with all dependencies:',
                                        [Roles.ADMIN, Roles.SUPER_ADMIN], select_data)
    fetch_all_incidents = DMLQueriesValues('Display a list of all incidents with associated users',
                                           'List of all incidents with associated users:',
                                           [Roles.ADMIN, Roles.SUPER_ADMIN], select_data)
    fetch_incident_by_id = DMLQueriesValues('Display incident by id',
                                            'Incident data with ID = 1?:',
                                            [Roles.ADMIN, Roles.SUPER_ADMIN], select_data)
    fetch_all_active_incidents = DMLQueriesValues('Display a list of all active incidents with associated users',
                                                  'List of all active incidents with associated users:',
                                                  [Roles.ADMIN, Roles.SUPER_ADMIN], select_data)
    add_user = DMLQueriesValues('Create a new user with a profile',
                                'A new user with ID = 7? with a profile created:',
                                [Roles.ADMIN, Roles.SUPER_ADMIN], execute_script)
    update_user_by_id = DMLQueriesValues('Update user data by id with profile',
                                         'User data with ID = 10? with profile updated:',
                                         [Roles.ADMIN, Roles.SUPER_ADMIN], execute_script)
    del_user = DMLQueriesValues('Delete user by id with all dependencies',
                                'User with ID = 1? and with all dependencies deleted',
                                [Roles.ADMIN, Roles.SUPER_ADMIN], execute_script)
    subscribe_service_by_id = DMLQueriesValues('Subscribe user by id to the service by id',
                                               'User with ID = 1? subscribed to the service with ID = 2?',
                                               [Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USER], execute_script)
    unsubscribe_service_by_id = DMLQueriesValues('Unsubscribe user by id from the service by id',
                                                 'User with ID = 1? unsubscribed from the service with ID = 2?',
                                                 [Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USER], execute_script)
    create_incident = DMLQueriesValues('Create an incident (ticket)',
                                       'Incident (ticket) with ID = 1? created',
                                       [Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USER], execute_script)
    close_incident_by_id = DMLQueriesValues('Set incident (ticket) status as completed',
                                            'Incident (ticket) with ID = 1? completed',
                                            [Roles.ADMIN, Roles.SUPER_ADMIN], execute_script)
    exit = DMLQueriesValues('Exit', '', [Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USER], None)


def database_manipulation(func, args: tuple):
    """ Выполняет заданную функцию с заданными аргументами
    Arguments:
        func: исполняемая функция
        args: кортеж аргументов
    Returns:
        результат выполнения функции """

    sqlite_connection = None
    result = None
    try:
        sqlite_connection = sqlite3.connect('lesson_11__task_3_Services.sqlite')
        cursor = sqlite_connection.cursor()
        full_arg = [cursor]
        full_arg.extend(args)
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


def add_new_records(args: tuple):
    """ Добавляет новые записи в таблицу БД
    Arguments:
        args: список аргументов, структура списка:
            args[0] - sqlite3.Cursor object
            args[1] - SQL query string
            args[2] - values
    Returns:
        True """
    args[0].execute("BEGIN TRANSACTION;")
    args[0].executemany(args[1], args[2])
    return True


def get_field_list(list_of_tuples: list) -> list:
    """ Извлекает первый список из возвращаемого кортежа после выполнения запроса на выборку данных
    Arguments:
        list_of_tuples: кортеж, возвращаемый методом fetch...
    Returns:
        первый список из кортежа"""
    if list_of_tuples:
        return [element[0] for element in list_of_tuples]
    else:
        return []


def database_initialization(queries: dict):
    """ Создает в БД необходимые таблицы, заполняет их тестовыми данными и задает значения внешних ключей таблиц
    Arguments:
        queries: список соответствующих запросов """

    database_manipulation(execute_script, ("PRAGMA foreign_keys = ON;",))

    # Создание таблиц в базе данных

    # sql_script = ''
    for table_name in TABLE_ORDER:
        sql_script = ' '.join(queries.get(table_name).get('create'))
        database_manipulation(execute_script, (sql_script,))

    # Заполнение таблиц БД тестовыми данными

    # user_role
    table_data = [('USER', fake.sentence(nb_words=3)),
                  ('ADMIN', fake.sentence(nb_words=3)),
                  ('SUPER_ADMIN', fake.sentence(nb_words=3))]
    database_manipulation(add_new_records, (' '.join(queries.get('user_role').get('add')), table_data))
    id_lists['user_role'] = get_field_list(
        database_manipulation(select_data, (queries.get('user_role').get('get_ids'),)))

    # user
    table_data.clear()
    for _ in range(QUANTITIES.get('user')):
        table_data.append((fake.user_name(),
                           fake.password(length=choice(range(7, 12)), special_chars=False),
                           choice(id_lists['user_role'])))
    database_manipulation(add_new_records, (' '.join(queries.get('user').get('add')), table_data))
    id_lists['user'] = get_field_list(database_manipulation(select_data, (queries.get('user').get('get_ids'),)))

    # profile
    table_data.clear()
    available_user_id_list = list(id_lists['user'])
    for _ in range(QUANTITIES.get('user')):
        random_user_id = choice(available_user_id_list)
        available_user_id_list.remove(random_user_id)
        table_data.append((fake.first_name(),
                           fake.last_name(),
                           fake.email(),
                           fake.phone_number(),
                           fake.postcode(),
                           random_user_id))
    database_manipulation(add_new_records, (' '.join(queries.get('profile').get('add')), table_data))
    id_lists['profile'] = get_field_list(database_manipulation(select_data, (queries.get('profile').get('get_ids'),)))

    # service
    table_data.clear()
    for i in range(QUANTITIES.get('service')):
        table_data.append((f'Service № {i + 1}',
                           choice([0, 1]),
                           round(random() * 100, 2),
                           randint(1, 100)))
    database_manipulation(add_new_records, (' '.join(queries.get('service').get('add')), table_data))
    id_lists['service'] = get_field_list(database_manipulation(select_data, (queries.get('service').get('get_ids'),)))

    # user_services
    table_data.clear()
    for item in id_lists['user']:
        for _ in range(randint(2, 5)):
            table_data.append((item, choice(id_lists['service'])))
    table_data = list(set(table_data))
    database_manipulation(add_new_records, (' '.join(queries.get('user_services').get('add')), table_data))

    # incident
    table_data.clear()
    service_names = get_field_list(
        database_manipulation(select_data, (queries.get('service').get('get_serviceNames'),)))
    for _ in range(QUANTITIES.get('incident')):
        table_data.append((choice(service_names),
                           choice([0, 1]),
                           fake.paragraph(nb_sentences=3),
                           choice(id_lists['user'])))
    database_manipulation(add_new_records, (' '.join(queries.get('incident').get('add')), table_data))
    id_lists['incident'] = get_field_list(database_manipulation(select_data, (queries.get('incident').get('get_ids'),)))


def input_integer(input_str: str, valid_values: list) -> int:
    """ Ввод целого числа с валидацией значения
    Arguments:
        input_str (str): текстовая метка
        valid_values (list): список допустимых значений
    Returns:
        int - введенное значение """
    result = None
    while result is None:
        try:
            result = int(input(input_str))
            if result not in valid_values:
                result = None
                raise ValueError
        except ValueError:
            print(f'Wrong input! Please enter an integer from valid values: {valid_values}')
            continue
    return result


def user_menu(header: str, items: enum.EnumMeta, role_to_display: enum.Enum = None) -> enum.Enum:
    """ Создает меню в консоли и обрабатывает выбор пользователя с проверкой корректности введенного значения
    Arguments:
        header (str): заголовок меню
        items (enum.EnumMeta): список пунктов меню
        role_to_display (enum.Enum): определяет доступные действия для заданной роли пользователя
    Returns:
        enum.Enum - выбранное действие """
    result = None
    display_menu_items = []
    while result is None:
        print(header)
        number = 1
        for item in items:
            if role_to_display is not None and item.value.roles:
                if role_to_display not in item.value.roles:
                    continue
            print(f'{str(number).rjust(2, " ")}. {item.value.menu_item}')
            display_menu_items.append(item)
            number += 1
        print()
        item_choice = input_integer('Enter your choice: ', list(range(1, number)))
        result = display_menu_items[item_choice - 1]
        return result


def get_dml_query(name: str) -> str:
    """ Выбирает из списка запрос с соответствующим именем для заданного действия
    Arguments:
        name (str): имя действия
    Returns:
        str - строка запроса """
    return ' '.join(query_list.get('DMLQueries').get(name))


def make_replacements(source_string: str, replacements: dict) -> str:
    """ Производит замены шаблонов в строке запроса и в строке отчета на реальные значения
    Arguments:
        source_string (str): строка с шаблонами вместо значений
        replacements (dict): словарь замен
    Returns:
        str - строка с реальными значениями вместо шаблонов """
    for old_str, new_str in replacements.items():
        source_string = source_string.replace(old_str, new_str)
    return source_string


if __name__ == '__main__':

    # Чтение запросов из файла
    with open('lesson_11__task_3_queries.json', 'r') as file:
        query_list = json.load(file)

    # инициализация
    fake = Faker()
    id_lists = dict.fromkeys(['user', 'user_role', 'profile', 'service', 'incident'])
    database_initialization(query_list)

    # выбор роли пользователя
    user_role = user_menu('\n   Select your database role: ', Roles)
    if user_role == Roles.EXIT:
        exit(0)
    oper_args = []
    oper_replacements = {}

    # основной цикл работы с БД
    while True:
        user_choice = user_menu('\n    Select operation: ', DMLQueries, user_role)
        oper_args.clear()
        oper_replacements.clear()
        oper_func = None
        oper_status = ''
        user_id = None
        profile_id = None
        if user_choice == DMLQueries.exit:
            break

        # input parameters
        if user_choice in [DMLQueries.fetch_user_by_id,
                           DMLQueries.update_user_by_id,
                           DMLQueries.del_user,
                           DMLQueries.subscribe_service_by_id,
                           DMLQueries.unsubscribe_service_by_id]:
            oper_replacements['1?'] = str(input_integer('Enter user ID: ', id_lists['user']))
        if user_choice in [DMLQueries.subscribe_service_by_id,
                           DMLQueries.unsubscribe_service_by_id]:
            oper_replacements['2?'] = str(input_integer('Enter service ID: ', id_lists['service']))
        if user_choice in [DMLQueries.fetch_incident_by_id,
                           DMLQueries.close_incident_by_id]:
            oper_replacements['1?'] = str(input_integer('Enter incident ID: ', id_lists['incident']))
        if user_choice == DMLQueries.add_user:
            oper_replacements.update({'1?': str(max(id_lists["profile"]) + 1), '2?': f"'{fake.first_name()}'",
                                      '3?': f"'{fake.last_name()}'", '4?': f"'{fake.email()}'",
                                      '5?': f"'{fake.phone_number()}'",
                                      '6?': f"'{fake.postcode()}'", '7?': str(max(id_lists["user"]) + 1),
                                      '8?': str(max(id_lists["user"]) + 1), '9?': f"'{fake.user_name()}'",
                                      '10?': f"'{fake.password(length=choice(range(7, 12)), special_chars=False)}'",
                                      '11?': str(choice(id_lists['user_role']))})
            oper_replacements = dict(sorted(oper_replacements.items(), key=lambda x: x[0]))
        if user_choice == DMLQueries.create_incident:
            service_name_list = get_field_list(
                database_manipulation(select_data, (query_list.get('service').get('get_serviceNames'),)))
            oper_replacements.update({'1?': str(max(id_lists["incident"]) + 1),
                                      '2?': f"'{choice(service_name_list)}'",
                                      '3?': '1',
                                      '4?': f"'{fake.paragraph(nb_sentences=3)}'",
                                      '5?': str(choice(id_lists['user']))})
        if user_choice in [DMLQueries.update_user_by_id, DMLQueries.del_user]:
            oper_args.append(make_replacements(get_dml_query(DMLQueries.fetch_user_by_id.name), oper_replacements))
            data = database_manipulation(select_data, tuple(oper_args))[0]
            if data:
                user_id = data[0]
                profile_id = data[1]
                if user_choice == DMLQueries.update_user_by_id:
                    oper_replacements.update({'1?': f"'{fake.first_name()}'", '2?': f"'{fake.last_name()}'",
                                              '3?': f"'{fake.email()}'", '4?': f"'{fake.phone_number()}'",
                                              '5?': f"'{fake.postcode()}'", '6?': str(profile_id),
                                              '7?': f"'{fake.user_name()}'",
                                              '8?': f"'{fake.password(length=choice(range(7, 12)), special_chars=False)}'",
                                              '9?': str(choice(id_lists['user_role'])), '10?': str(user_id)})
                    oper_replacements = dict(sorted(oper_replacements.items(), key=lambda x: x[0]))
                oper_args.clear()

        # function choice
        oper_func = user_choice.value.oper_func

        # set args and status
        oper_args.append(make_replacements(get_dml_query(user_choice.name), oper_replacements))
        oper_status = make_replacements(user_choice.value.report, oper_replacements)

        # databse manipulation
        data = database_manipulation(oper_func, tuple(oper_args))

        # post checking
        if user_choice == DMLQueries.add_user:
            if data:
                id_lists["user"].append(max(id_lists["user"]) + 1)
                id_lists["profile"].append(max(id_lists["profile"]) + 1)
            else:
                oper_status = 'User creation error'
        if user_choice == DMLQueries.del_user:
            if data:
                id_lists["user"].remove(user_id)
                id_lists["profile"].remove(profile_id)
            else:
                oper_status = 'User deletion error'
        if user_choice == DMLQueries.create_incident:
            if data:
                id_lists["incident"].append(max(id_lists["incident"]) + 1)
            else:
                oper_status = 'Incident creation error'
        if user_choice == DMLQueries.update_user_by_id:
            if not data:
                oper_status = 'User data update error'

        # report
        print()
        print(oper_status)
        if all([data is not None, data is not True]):
            pprint(data)
        input('Press any key')
