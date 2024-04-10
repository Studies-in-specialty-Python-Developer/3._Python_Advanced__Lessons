""" Урок 3, завдання 5
Для таблиці «матеріалу» з додаткового завдання створіть функцію користувача, яка приймає
необмежену кількість полів і повертає їх конкатенацію.
"""

import json


def make_material_string(*args):
    material_string = ''
    for arg in args:
        material_string += arg['material']
    return material_string


with open('lesson_3__task_4_materials.json', 'r') as jsf:
    materials = json.load(jsf)
print(make_material_string(*materials))
