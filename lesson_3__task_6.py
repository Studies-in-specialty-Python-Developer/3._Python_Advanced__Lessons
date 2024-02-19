""" Урок 3, завдання 6
Створіть функцію, яка формує CSV-файл на основі даних, введених користувачем через консоль.
Файл має містити такі стовпчики: імена, прізвища, дати народження та місто проживання. Реалізуйте
можливості перезапису цього файлу, додавання нових рядків до наявного файлу, рядкового читання
з файлу та конвертації всього вмісту у формати XML та JSON.
"""

import xml.etree.ElementTree as Et
import csv
import json
from faker import Faker

FILE_NAME = 'lesson_3__task_6_example'


def create_str():
    return [fake.first_name(), fake.last_name(), fake.date(), fake.city()]


def create_csv(row_number):
    with open(FILE_NAME + '.csv', 'w', newline='') as file:
        data = csv.writer(file)
        data.writerow(['name', 'surname', 'birthday', 'city'])
        for _ in range(row_number):
            data.writerow(create_str())


def add_rows_to_csv(row_number):
    with open(FILE_NAME + '.csv', 'a', newline='') as file:
        data = csv.writer(file)
        for _ in range(row_number):
            data.writerow(create_str())


def read_csv():
    with open(FILE_NAME + '.csv', 'r') as file:
        data = csv.reader(file)
        for row in data:
            print(row)


def convert_csv_to_xml():
    with open(FILE_NAME + '.csv', 'r') as file:
        csv_data = csv.reader(file)
        field_names = None
        root = Et.Element('data')
        for row_num, row in enumerate(csv_data):
            if row_num == 0:
                field_names = row
            else:
                record = Et.SubElement(root, 'record')
                for i in range(len(field_names)):
                    Et.SubElement(record, f'{field_names[i]}').text = row[i]
        tree = Et.ElementTree(root)
        tree.write(FILE_NAME + '.xml')
    return tree


def convert_csv_to_json():
    with open(FILE_NAME + '.csv', 'r') as file:
        csv_data = csv.DictReader(file)
        json_data = []
        for row in csv_data:
            json_data.append(row)
    with open(FILE_NAME + '.json', mode='w') as file:
        json.dump(json_data, file, indent=4)
    return json.dumps(json_data)


# name = input('Enter name: ')
# surname = input('Enter surname: ')
# birthday = input('Enter birthday: ')
# city = input('Enter city: ')

fake = Faker()
create_csv(3)
add_rows_to_csv(2)
read_csv()
convert_csv_to_xml()
convert_csv_to_json()
