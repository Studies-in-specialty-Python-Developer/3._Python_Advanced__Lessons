""" Урок 9, завдання 3
Створити клас, у який дозволяє зберігати дані про студента:
- ім'я;
- прізвище;
- вік;
- середній бал.
Створіть список з 10 студентів-інстансів даного класу та протестуйте валідність даних використовуючи пакет unittest.
"""

import unittest
from time import sleep

from lesson_9__task_3 import students


class TestStudent(unittest.TestCase):
    def test_name(self):
        for student in students:
            self.assertIsInstance(student.name, str)
            self.assertGreater(len(student.name), 0)

    def test_surname(self):
        for student in students:
            self.assertIsInstance(student.surname, str)
            self.assertGreater(len(student.surname), 0)

    @unittest.expectedFailure
    def test_age(self):
        for student in students:
            self.assertIsInstance(student.age, int, student.surname)
            self.assertGreaterEqual(student.age, 18, student.surname)
            self.assertLessEqual(student.age, 28, student.surname)

    @unittest.expectedFailure
    def test_average_grade(self):
        for student in students:
            self.assertIsInstance(student.average_grade, float, student.surname)
            self.assertGreaterEqual(student.average_grade, 0.0, student.surname)
            self.assertLessEqual(student.average_grade, 5.0, student.surname)


if __name__ == '__main__':
    unittest.main()
