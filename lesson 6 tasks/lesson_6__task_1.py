""" Урок 6, завдання 1
Створіть функцію для обчислення факторіала числа. Запустіть декілька завдань, використовуючи
ThreadPoolExecutor, і заміряйте швидкість їхнього виконання, а потім заміряйте швидкість обчислення,
використовуючи той же набір завдань на ProcessPoolExecutor. Як приклади використовуйте останні
значення, від мінімальних і до максимально можливих, щоб побачити приріст або втрату продуктивності.
"""

import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def run_by_executor_map(executor_class, max_workers=3):
    executor = executor_class(max_workers=max_workers)
    start_time = time.time()
    params = [100, 200, 300, 400, 500]
    executor.map(factorial, params)
    print(f'max_workers: {max_workers}. Time for {executor_class.__name__}: {time.time() - start_time}')


if __name__ == '__main__':
    run_by_executor_map(ThreadPoolExecutor, max_workers=1)
    run_by_executor_map(ThreadPoolExecutor, max_workers=2)
    run_by_executor_map(ThreadPoolExecutor, max_workers=3)
    run_by_executor_map(ThreadPoolExecutor, max_workers=4)
    run_by_executor_map(ThreadPoolExecutor, max_workers=5)
    print()
    run_by_executor_map(ProcessPoolExecutor, max_workers=1)
    run_by_executor_map(ProcessPoolExecutor, max_workers=2)
    run_by_executor_map(ProcessPoolExecutor, max_workers=3)
    run_by_executor_map(ProcessPoolExecutor, max_workers=4)
    run_by_executor_map(ProcessPoolExecutor, max_workers=5)
