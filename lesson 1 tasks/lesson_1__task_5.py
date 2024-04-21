""" Урок 1, завдання 5
Створіть список цілих чисел. Отримайте список квадратів непарних чисел із цього списку.
"""

integers = list(range(-10, 10, 1))
squares = [x ** 2 for x in filter(lambda x: x % 2 != 0, integers)]
print(squares)
