""" Урок 3, завдання 3
Попрацюйте зі створенням власних діалектів, довільно вибираючи правила для CSV-файлів.
Зареєструйте створені діалекти та попрацюйте, використовуючи їх зі створенням/читанням файлом.
"""

import csv

# Считывание из файла и вывод CSV как словарь
with open('lesson_3__task_3_example.csv', 'r', newline='') as f:
    data = csv.DictReader(f)
    for row in data:
        print(f'name = {row.get("name")}, price = {row.get("price")}')
        print(f'{data.line_num}: {row}')
print()

# Считывание из файла и вывод CSV как таблица
data_rows = []
with open('lesson_3__task_3_example.csv', 'r', newline='') as f:
    data = csv.reader(f)
    for row in data:
        print(f'{data.line_num}: {row}')
        data_rows.append(row)
print()

# Распознавание диалекта с помощью csv.Sniffer()
sniffer = csv.Sniffer()
with open('lesson_3__task_3_example.csv', 'r', newline='') as f:
    data = f.read()
    dialect = sniffer.sniff(data)
    print('Наличие строки заголовков:', sniffer.has_header(data))
    print('Разделитель колонок:', dialect.delimiter)
    print('Экранирование кавычек:', dialect.doublequote)
    print('Экранирование чего-то еще:', dialect.quoting)
print()


# Создание и применение своего диалекта
class MyDialect(csv.Dialect):
    delimiter = '!'
    quoting = csv.QUOTE_ALL
    quotechar = "_"
    lineterminator = '\n'


csv.register_dialect('my_dialect', MyDialect)

with open('lesson_3__task_3_output.csv', 'w') as f:
    writer = csv.writer(f, dialect='my_dialect')
    for row in data_rows:
        writer.writerow(row)

with open('lesson_3__task_3_output.csv', 'r', newline='') as f:
    data = csv.DictReader(f, dialect='my_dialect')
    for row in data:
        print(row)
