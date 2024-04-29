""" Урок 9, завдання 3
Створити клас, у який дозволяє зберігати дані про студента:
- ім'я;
- прізвище;
- вік;
- середній бал.
Створіть список з 10 студентів-інстансів даного класу та протестуйте валідність даних використовуючи пакет unittest.
"""

from faker import Faker


class Student:
    def __init__(self, name, surname, age, average_grade):
        self.name = name
        self.surname = surname
        self.age = age
        self.average_grade = average_grade

    def __str__(self):
        return f'{self.name} {self.surname}, {self.age}, {self.average_grade}'


fake_ua = Faker('uk_UA')
students = []
for _ in range(10):
    students.append(
        Student(fake_ua.first_name(), fake_ua.last_name(), fake_ua.random_int(18, 30),
                round(fake_ua.random_int(0, 60) / 10, 1)))
    print(students[_])
