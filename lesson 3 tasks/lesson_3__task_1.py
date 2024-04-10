""" Урок 3, завдання 1
Створіть прості словники та конвертуйте їх у JSON. Збережіть JSON у файлі та спробуйте
завантажити дані з файлу.
"""

import json

person_1 = {
    'name': 'John',
    'age': 30,
    'city': 'New York',
    'hobbies': ['reading', 'hiking', 'gaming'],
    'is_married': False,
    'children': None,
}

person_2 = {
    'name': 'Jane',
    'age': 25,
    'city': 'Los Angeles',
    'hobbies': ['cooking', 'dancing', 'traveling'],
    'is_married': True,
    'children': ['Alice', 'Bob'],
}

person_3 = {
    'name': 'Bob',
    'age': 35,
    'city': 'Chicago',
    'hobbies': ['football', 'basketball', 'baseball'],
    'is_married': False,
    'children': None,
}

person_list = [person_1, person_2, person_3]
person_list_json = json.dumps(person_list, indent=4)
print(person_list)
print()
print(person_list_json)

with open('person_list.json', 'w') as jsf:
    json.dump(person_list, jsf, indent=4)

with open('person_list.json', 'r') as jsf:
    person_list_file = json.load(jsf)

print()
print(person_list_file)
