""" Урок 7, завдання 1
Створіть функцію, яка приймає список з елементів типу int, а повертає новий список з рядкових
значень вихідного масиву. Додайте анотацію типів для вхідних і вислідних значень функції.
"""


def convert_int_to_str(lst_int: list[int]) -> list[str]:
    return list(map(str, lst_int))


if __name__ == '__main__':
    lst = [1, 2, 3, 4, 5]
    print(lst)
    print(convert_int_to_str([1, 2, 3, 4, 5]))
