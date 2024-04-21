""" Урок 1, завдання 3
Напишіть програму яка буде виводити 25 перших чисел Фібоначі, використовуючи для цього три наведені в тексті
заняття функції — без кешу, з кешем довільної довжини, з кешем з модуля functools з максимальною кількістю
10 елементів та з кешем з модуля functools з максимальною кількістю 16 елементів.
"""

import functools


def fibonacci(num):
    if num in [1, 2]:
        return num - 1
    return fibonacci(num - 1) + fibonacci(num - 2)


def f1(n):
    for i in range(1, n + 1):
        print(fibonacci(i), end=' ')
    print()


def f2(n):
    for i in range(1, n + 1):
        print(functools.cache(fibonacci)(i), end=' ')
    print()


def f3(n):
    for i in range(1, n + 1):
        print(functools.lru_cache(10)(fibonacci)(i), end=' ')
    print()


def f4(n):
    for i in range(1, n + 1):
        print(functools.lru_cache(16)(fibonacci)(i), end=' ')
    print()


if __name__ == '__main__':
    f1(25)
    f2(25)
    f3(25)
    f4(25)
