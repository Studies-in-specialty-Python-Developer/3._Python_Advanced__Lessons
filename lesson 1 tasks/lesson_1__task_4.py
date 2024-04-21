""" Урок 1, завдання 4
За допомогою написаного Вами декоратору заміряйте та порівняйте швидкість роботи цих 4 варіантів.
"""

from lesson_1__task_2 import stopwatch
from lesson_1__task_3 import f1, f2, f3, f4

f1 = stopwatch(f1)
f2 = stopwatch(f2)
f3 = stopwatch(f3)
f4 = stopwatch(f4)

f1(25)
f2(25)
f3(25)
f4(25)
