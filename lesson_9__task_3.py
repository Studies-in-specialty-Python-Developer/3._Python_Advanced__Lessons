""" Урок 9, завдання 3
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

TABLE_ORDER = ('user_role', 'user', 'profile', 'service', 'user_services', 'incident')

QUANTITIES = {
    'user': 20,
    'user_role': 3,
    'service': 10,
    'incident': 50,
}


class Roles(enum.Enum):
    USER = ('USER', [])
    ADMIN = ('ADMIN', [])
    SUPER_ADMIN = ('SUPER ADMIN', [])
    EXIT = ('EXIT', [])


class DMLQueries(enum.Enum):
    fetch_all_users = ('Display a list of all users with all dependencies', [Roles.ADMIN, Roles.SUPER_ADMIN])
    fetch_user_by_id = ('Display user by id with all dependencies', [Roles.ADMIN, Roles.SUPER_ADMIN])
    fetch_all_incidents = ('Display a list of all incidents and associated users', [Roles.ADMIN, Roles.SUPER_ADMIN])
    fetch_incident_by_id = ('Display incident by id', [Roles.ADMIN, Roles.SUPER_ADMIN])
    fetch_all_active_incidents = (
        'Display a list of all active incidents and associated users', [Roles.ADMIN, Roles.SUPER_ADMIN])
    add_user = ('Create a new user with a profile', [Roles.ADMIN, Roles.SUPER_ADMIN])
    update_user_by_id = ('Update user data by id with profile', [Roles.ADMIN, Roles.SUPER_ADMIN])
    del_user = ('Delete user by id with all dependencies', [Roles.ADMIN, Roles.SUPER_ADMIN])
    subscribe_service_by_id = ('Subscribe to the service by id', [Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USER])
    unsubscribe_service_by_id = ('Unsubscribe from the service by id', [Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USER])
    create_incident = ('Create an incident (ticket)', [Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USER])
    close_incident = ('Set incident status as completed', [Roles.ADMIN, Roles.SUPER_ADMIN])
    exit = ('Exit', [Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USER])


def database_manipulation(func, args: tuple):
    sqlite_connection = None
    result = None
    try:
        sqlite_connection = sqlite3.connect('lesson_9__task_3_Services.sqlite')
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


def execute_script(args: tuple):
    # args[0] - sqlite3.Cursor object
    # args[1] - SQL script string
    args[0].execute("BEGIN TRANSACTION;")
    args[0].executescript(args[1])
    return True


def select_data(args: tuple):
    # args[0] - sqlite3.Cursor object
    # args[1] - SQL query string
    args[0].execute(args[1], args[2:])
    return args[0].fetchall()


def add_new_records(args: tuple):
    # args[0] - sqlite3.Cursor object
    # args[1] - SQL query string
    # args[2] - values
    args[0].execute("BEGIN TRANSACTION;")
    args[0].executemany(args[1], args[2])
    return True


def get_field_list(list_of_tuples: list) -> list:
    if list_of_tuples:
        return [element[0] for element in list_of_tuples]
    else:
        return []


def database_initialization(queries: dict):
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


def user_menu(header: str, items: enum.EnumMeta, role_to_display: enum.Enum = None):
    result = None
    display_menu_items = []
    while result is None:
        print(header)
        number = 1
        for item in items:
            if all([role_to_display is not None, item.value[1]]):
                if role_to_display not in item.value[1]:
                    continue
            print(f'{str(number).rjust(2, " ")}. {item.value[0]}')
            display_menu_items.append(item)
            number += 1
        print()
        item_choice = input_integer('Enter your choice: ', list(range(1, number + 1)))
        result = display_menu_items[item_choice - 1]
        return result


if __name__ == '__main__':
    with open('lesson_9__task_3_queries.json', 'r') as file:
        query_list = json.load(file)
    fake = Faker()

    # id_lists = dict.fromkeys(['user', 'user_role', 'profile', 'service', 'incident'])
    #
    # database_initialization(query_list)

    id_lists = {'user': get_field_list(database_manipulation(select_data, (query_list.get('user').get('get_ids'),))),
                'user_role': get_field_list(
                    database_manipulation(select_data, (query_list.get('user_role').get('get_ids'),))),
                'profile': get_field_list(
                    database_manipulation(select_data, (query_list.get('profile').get('get_ids'),))),
                'service': get_field_list(
                    database_manipulation(select_data, (query_list.get('service').get('get_ids'),))),
                'incident': get_field_list(
                    database_manipulation(select_data, (query_list.get('incident').get('get_ids'),)))}

    user_role = user_menu('\n   Select your database role: ', Roles)
    if user_role == Roles.EXIT:
        exit(0)
    oper_args = []
    while True:
        user_choice = user_menu('\n   Select operation: ', DMLQueries, user_role)
        oper_args.clear()
        oper_func = None
        oper_status = ''
        if user_choice == DMLQueries.fetch_all_users:
            oper_args.append(' '.join(query_list.get('DMLQueries').get(user_choice.name)))
            oper_func = select_data
            oper_status = f'   {user_choice.value[0]}'
        elif user_choice == DMLQueries.fetch_user_by_id:
            oper_user_id = input_integer('Enter user ID: ', id_lists['user'])
            oper_args = [' '.join(query_list.get('DMLQueries').get(user_choice.name)), oper_user_id]
            oper_func = select_data
            oper_status = f'   {user_choice.value[0]}. User ID = {oper_user_id}'
        elif user_choice == DMLQueries.fetch_all_incidents:
            oper_args.append(' '.join(query_list.get('DMLQueries').get(user_choice.name)))
            oper_func = select_data
            oper_status = f'   {user_choice.value[0]}'
        elif user_choice == DMLQueries.fetch_incident_by_id:
            oper_incident_id = input_integer('Enter incident ID: ', id_lists['incident'])
            oper_args = [' '.join(query_list.get('DMLQueries').get(user_choice.name)), oper_incident_id]
            oper_func = select_data
            oper_status = f'   {user_choice.value[0]}. Incident ID = {oper_incident_id}'
        elif user_choice == DMLQueries.fetch_all_active_incidents:
            oper_args.append(' '.join(query_list.get('DMLQueries').get(user_choice.name)))
            oper_func = select_data
            oper_status = f'   {user_choice.value[0]}'
        elif user_choice == DMLQueries.add_user:
            oper_profile_id = max(id_lists["profile"]) + 1
            oper_user_id = max(id_lists["user"]) + 1
            sql_query = ' '.join(query_list.get('DMLQueries').get(user_choice.name))
            sql_query = sql_query.replace("VALUES (?, ?, ?, ?, ?, ?, ?)",
                                          f"VALUES ({oper_profile_id}, '{fake.first_name()}', "
                                          f"'{fake.last_name()}', '{fake.email()}', "
                                          f"'{fake.phone_number()}', '{fake.postcode()}', {oper_user_id})")
            sql_query = sql_query.replace("VALUES (?, ?, ?, ?)",
                                          f"VALUES ({oper_user_id}, '{fake.user_name()}', "
                                          f"'{fake.password(length=choice(range(7, 12)), special_chars=False)}', "
                                          f"{choice(id_lists['user_role'])})")
            data = database_manipulation(execute_script, (sql_query,))
            id_lists["profile"].append(oper_profile_id)
            id_lists["user"].append(oper_user_id)
            oper_args = [' '.join(query_list.get('DMLQueries').get('fetch_user_by_id')), oper_user_id]
            oper_func = select_data
            oper_status = f'   {user_choice.value[0]}'
        elif user_choice == DMLQueries.update_user_by_id:
            oper_user_id = input_integer('Enter user ID: ', id_lists['user'])
            oper_args.extend([' '.join(query_list.get('DMLQueries').get('fetch_user_by_id')), oper_user_id])
            data = database_manipulation(select_data, tuple(oper_args))[0]
            sql_query = ' '.join(query_list.get('DMLQueries').get(user_choice.name))
            sql_query = sql_query.replace(
                "firstName = ?, lastName = ?, email = ?, phoneNumber = ?, postalCode = ?",
                f"firstName = '{fake.first_name()}', lastName = '{fake.last_name()}', "
                f"email = '{fake.email()}', phoneNumber = '{fake.phone_number()}',"
                f"postalCode = '{fake.postcode()}'")
            sql_query = sql_query.replace("WHERE profile_id = ?;", f"WHERE profile_id = {data[1]};")
            sql_query = sql_query.replace(
                "user_name = ?, password = ?, user_role_id = ?",
                f"user_name = '{fake.user_name()}', "
                f"password = '{fake.password(length=choice(range(7, 12)), special_chars=False)}', "
                f"user_role_id = {choice(id_lists['user_role'])}")
            sql_query = sql_query.replace("WHERE user_id = ?;", f"WHERE user_id = {data[0]};")
            oper_args.append(sql_query)
            database_manipulation(execute_script, (sql_query,))
            oper_args = [' '.join(query_list.get('DMLQueries').get('fetch_user_by_id')), oper_user_id]
            oper_func = select_data
            oper_status = f'   {user_choice.value[0]}. User ID = {oper_user_id}\nIt was:\n{data}\nIt became:'
        elif user_choice == DMLQueries.del_user:
            oper_user_id = input_integer('Enter user ID: ', id_lists['user'])
            sql_query = ' '.join(query_list.get('DMLQueries').get(user_choice.name))
            sql_query = sql_query.replace("user_id = ?;", f"user_id = {oper_user_id};")
            oper_args = [sql_query]
            oper_func = execute_script
            oper_status = f'   {user_choice.value[0]}. User ID = {oper_user_id}'
        elif user_choice == DMLQueries.subscribe_service_by_id:
            oper_user_id = input_integer('Enter user ID: ', id_lists['user'])
            oper_service_id = input_integer('Enter service ID: ', id_lists['service'])
            sql_query = ' '.join(query_list.get('DMLQueries').get(user_choice.name))
            sql_query = sql_query.replace("user_id = ? AND service_id = ?",
                                          f"user_id = {oper_user_id} AND service_id = {oper_service_id}")
            sql_query = sql_query.replace("VALUES (?, ?)",
                                          f"VALUES ({oper_user_id}, {oper_service_id})")
            oper_args = [sql_query]
            oper_func = execute_script
            oper_status = f'   {user_choice.value[0]}. User ID = {oper_user_id}, Service ID = {oper_service_id}'
        elif user_choice == DMLQueries.unsubscribe_service_by_id:
            oper_user_id = input_integer('Enter user ID: ', id_lists['user'])
            oper_service_id = input_integer('Enter service ID: ', id_lists['service'])
            sql_query = ' '.join(query_list.get('DMLQueries').get(user_choice.name))
            sql_query = sql_query.replace("user_id = ? AND service_id = ?",
                                          f"user_id = {oper_user_id} AND service_id = {oper_service_id}")
            oper_args = [sql_query]
            oper_func = execute_script
            oper_status = f'   {user_choice.value[0]}. User ID = {oper_user_id}, Service ID = {oper_service_id}'
        elif user_choice == DMLQueries.create_incident:
            oper_incident_id = max(id_lists["incident"]) + 1
            service_name_list = get_field_list(
                database_manipulation(select_data, (query_list.get('service').get('get_serviceNames'),)))
            sql_query = ' '.join(query_list.get('DMLQueries').get(user_choice.name))
            data = database_manipulation(add_new_records, (sql_query, ((oper_incident_id,
                                                                        choice(service_name_list),
                                                                        1,
                                                                        fake.paragraph(nb_sentences=3),
                                                                        choice(id_lists['user'])),)))
            id_lists["incident"].append(oper_incident_id)
            oper_args = [' '.join(query_list.get('DMLQueries').get('fetch_incident_by_id')), oper_incident_id]
            oper_func = select_data
            oper_status = f'   {user_choice.value[0]}. Incident ID = {oper_incident_id}'
        elif user_choice == DMLQueries.close_incident:
            oper_incident_id = input_integer('Enter incident ID: ', id_lists['incident'])
            sql_query = ' '.join(query_list.get('DMLQueries').get(user_choice.name))
            sql_query = sql_query.replace("incident_id = ?", f"incident_id = {oper_incident_id}")
            # TODO реорганизовать основной цикл
            database_manipulation(execute_script, (sql_query,))
            oper_args = [' '.join(query_list.get('DMLQueries').get('fetch_incident_by_id')), oper_incident_id]
            oper_func = select_data
            oper_status = f'   {user_choice.value[0]}. Incident ID = {oper_incident_id}'
        elif user_choice == DMLQueries.exit:
            break
        data = database_manipulation(oper_func, tuple(oper_args))
        print()
        print(oper_status)
        if all([data is not None, data is not True]):
            pprint(data)
        input('Press any key')
