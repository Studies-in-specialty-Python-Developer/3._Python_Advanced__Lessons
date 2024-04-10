""" Урок 3, завдання 7
Створіть таблицю «матеріали» з таких полів: ідентифікатор, вага, висота та додаткові характеристики
матеріалу. Поле «додаткові характеристики матеріалу» має зберігати у собі масив, кожен елемент
якого є кортежем із двох значень: перше – назва характеристики, а друге – її значення.
"""

materials = [
    {"ID": 1, "material": "steel", "weight": 7800, "heigth": 1, "added_traits": [("charact_1", 1), ("charact_2", 2)]},
    {"ID": 2, "material": "copper", "weight": 8920, "heigth": 1, "added_traits": [("charact_1", 1), ("charact_2", 2)]}
]

print(materials)

# An example of such a table in json format is provided in the file - lesson_3__task_4_materials.json
