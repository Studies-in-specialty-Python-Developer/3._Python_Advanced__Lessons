""" Урок 1, завдання 4
Створіть звичайну функцію множення двох чисел. Частково застосуйте її до одного аргументу. Створіть
каррувану функцію множення двох чисел. Частково застосуйте її до одного аргументу.
"""

from functools import partial


def multiply(a, b):
    return a * b


def multiply_1(a):
    def multiply_2(b):
        return a * b

    return multiply_2


print('   Partitial function examle')

multiply_partial = partial(multiply, a=2)
print(multiply_partial(b=3))
multiply_partial = partial(multiply, 2)
print(multiply_partial(5))

print('   Carried function examle')

multiply_carried = multiply_1(2)
print(multiply_carried(3))
print(multiply_1(2)(5))
