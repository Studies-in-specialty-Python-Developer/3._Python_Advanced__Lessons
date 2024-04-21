""" Урок 1, завдання 6
Створіть функцію-генератор чисел Фібоначчі. Застосуйте до неї декоратор, який залишатиме в
послідовності лише парні числа.
"""


def even_fibonacci(func):
    def even_numbers():
        for number in func():
            if number % 2 == 0:
                yield number

    return even_numbers


@even_fibonacci
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


fib = fibonacci()
for i in range(10):
    print(next(fib))
