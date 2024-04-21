""" Урок 1, завдання 2
Напишіть декоратор, який буде заміряти час виконання для наданої функції.
"""

import time


def stopwatch(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'Function {func.__name__} executes in {end - start} seconds')
        return result

    return wrapper
