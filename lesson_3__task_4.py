""" Урок 3, завдання 4
Для таблиці «матеріалу» з додаткового завдання створіть користувальницьку агрегатну функцію, яка
рахує середнє значення ваги всіх матеріалів вислідної вибірки й округляє значення до цілого.
"""

import json


def average_weight(materials_list):
    total_weight = 0
    for material in materials_list:
        total_weight += material['weight']
    return round(total_weight / len(materials_list))


with open('lesson_3__task_4_materials.json', 'r') as jsf:
    materials = json.load(jsf)
print('Average weight:', average_weight(materials))
