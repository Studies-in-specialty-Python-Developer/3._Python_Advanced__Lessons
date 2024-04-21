""" Урок 11, завдання 2
Розробити програму, що реалізує довідник працівника відділу кадрів.
Університет складається з факультетів, факультети мають у своєму складі
кафедри та студентські групи. На кожній кафедрі є завідувач кафедри.
Деякі кафедри є профільними. Кожна група має студента-старосту та
профільну кафедру. Вважатимемо, що в університеті всі люди є
викладачами та/або студентами. Відомості про кожну людину мають
містити прізвище, ім'я, по батькові, стать, паспортні дані, місце
проживання. Для студентів додатково має бути інформація про батьків та
групу. Для викладачів додатково має бути інформація про кафедру та
посаду. Потрібно передбачити можливу ситуацію, коли одна й та сама
людина може бути одночасно студентом, батьком і викладачем. Один з
батьків може мати кілька дітей-студентів. Програма має завантажувати
довідник із жорсткого диска, редагувати всі дані, зберігати на диск. У
процесі роботи користувач програми має мати можливість перегляду таких
параметрів:
1. Список усіх студентів з можливістю сортування за ПІБ,
факультетом, групою, профільною кафедрою.
2. Список студентів, які не мають батьків, з можливістю
сортування за ПІБ, факультетом, групою, профільною кафедрою.
3. Список викладачів з можливістю сортування за ПІБ,
факультетом, кафедрою.
4. Список усіх завідувачів кафедр.
5. Список усіх груп без старост та кафедр без завідувачів.
6. Пошук у заданого батька всіх його дітей-студентів.
7. Список усіх викладачів, які мають дітей-студентів
"""

import sys
import traceback
import sqlite3
import json
from faker import Faker
from random import choice, choices

TABLE_ORDER = (
    'faculties', 'persons', 'students', 'relatives', 'teachers', 'students__relatives', 'chairs',
    'posts', 'chairs__teachers', 'groups', 'students__groups')

QUANTITIES = {
    'faculties': 2,
    'persons': 100,
    'students': 50,
    'relatives': 30,
    'teachers': 20,
    'chairs': 6,
    'groups': 10,
}


def database_manipulation(func, arg):
    sqlite_connection = None
    result = None
    try:
        sqlite_connection = sqlite3.connect('lesson_11__task_2_HR_guide.sqlite')
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


def add_new_records(args):
    # args[0] - sqlite3.Cursor object
    # args[1] - SQL query string
    # args[2] - values
    args[0].execute("BEGIN TRANSACTION;")
    args[0].executemany(args[1], args[2])


def get_id_list(list_of_tuples: list) -> list:
    return [element[0] for element in list_of_tuples]


with open('lesson_11__task_2_queries.json', 'r') as file:
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

# faculties
table_data = [('Economics',), ('Philology',)]
database_manipulation(add_new_records, (' '.join(queries.get('faculties').get('add')), table_data))
faculty_id_list = get_id_list(database_manipulation(select_data, ("SELECT faculty_id FROM faculties;",)))

# persons
table_data.clear()
person = []
for _ in range(QUANTITIES.get('persons')):
    sex = choice([0, 1])
    if sex:
        person = [fake.last_name_male(),
                  fake.first_name_male()]
        if choice([0, 1]):
            person.append(fake.first_name_male())
        else:
            person.append('')
    else:
        person = [fake.last_name_female(),
                  fake.first_name_female()]
        if choice([0, 1]):
            person.append(fake.first_name_female())
        else:
            person.append('')
    person.extend([sex, fake.passport_number(), fake.address()])
    table_data.append(tuple(person))
database_manipulation(add_new_records, (' '.join(queries.get('persons').get('add')), table_data))
person_id_list = get_id_list(database_manipulation(select_data, ("SELECT person_id FROM persons;",)))

# students
table_data.clear()
for _ in range(QUANTITIES.get('students')):
    table_data.append(choice(list(set(person_id_list) - set(table_data))))
database_manipulation(add_new_records, (' '.join(queries.get('students').get('add')), [(x,) for x in table_data]))
student_id_list = get_id_list(database_manipulation(select_data, ("SELECT student_id FROM students;",)))

# relatives
table_data.clear()
for _ in range(QUANTITIES.get('relatives')):
    table_data.append(choice(list(set(person_id_list) - set(table_data))))
database_manipulation(add_new_records, (' '.join(queries.get('relatives').get('add')), [(x,) for x in table_data]))
relative_id_list = get_id_list(database_manipulation(select_data, ("SELECT relative_id FROM relatives;",)))

# teachers
table_data.clear()
for _ in range(QUANTITIES.get('teachers')):
    table_data.append(choice(list(set(person_id_list) - set(table_data))))
database_manipulation(add_new_records, (' '.join(queries.get('teachers').get('add')), [(x,) for x in table_data]))
teacher_id_list = get_id_list(database_manipulation(select_data, ("SELECT teacher_id FROM teachers;",)))

# students__relatives
table_data.clear()
for item in student_id_list:
    relatives_number = choices([0, 1, 2], weights=[0.2, 0.3, 0.5])[0]
    relatives_set = set()
    while len(relatives_set) < relatives_number:
        relatives_set.add(choice(relative_id_list))
    for i in relatives_set:
        table_data.append((item, i))
    relatives_set.clear()
database_manipulation(add_new_records, (' '.join(queries.get('students__relatives').get('add')), table_data))

# chairs
table_data = [('Economic Theory', min(faculty_id_list), choice(person_id_list), 0),
              ('Accounting and Auditing', min(faculty_id_list), choice(person_id_list), 1),
              ('Management and Data Analysis', min(faculty_id_list), None, 1),
              ('English Language and Literature', max(faculty_id_list), choice(person_id_list), 0),
              ('Comparative Linguistics', max(faculty_id_list), choice(person_id_list), 1),
              ('Translation Theory and History', max(faculty_id_list), None, 1)]
database_manipulation(add_new_records, (' '.join(queries.get('chairs').get('add')), table_data))
chair_id_list = get_id_list(database_manipulation(select_data, ("SELECT chair_id FROM chairs;",)))
spec_chair_id_list = get_id_list(
    database_manipulation(select_data, ("SELECT chair_id FROM chairs WHERE specialized=TRUE;",)))

# posts
table_data = [('professor',), ('senior teacher',), ('teacher',), ('assistant',)]
database_manipulation(add_new_records, (' '.join(queries.get('posts').get('add')), table_data))
post_id_list = get_id_list(database_manipulation(select_data, ("SELECT post_id FROM posts;",)))

# chairs__teachers
table_data.clear()
for item in teacher_id_list:
    table_data.append((choice(chair_id_list), item, choice(post_id_list)))
database_manipulation(add_new_records, (' '.join(queries.get('chairs__teachers').get('add')), table_data))

# groups
table_data.clear()
group = []
for item in range(QUANTITIES.get('groups')):
    group = [f'Group № {item + 1}', choice(faculty_id_list), choice(spec_chair_id_list)]
    if choices([True, False], weights=[0.7, 0.3])[0]:
        group.append(choice(person_id_list))
    else:
        group.append(None)
    table_data.append(tuple(group))
database_manipulation(add_new_records, (' '.join(queries.get('groups').get('add')), table_data))
group_id_list = get_id_list(database_manipulation(select_data, ("SELECT group_id FROM groups;",)))

# students__groups
table_data.clear()
for item in student_id_list:
    table_data.append((item, choice(group_id_list)))
database_manipulation(add_new_records, (' '.join(queries.get('students__groups').get('add')), table_data))
