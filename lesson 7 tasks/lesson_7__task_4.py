""" Урок 7, завдання 4
Створіть кілька функцій:
1. Обчислення середнього арифметичного списку. Якщо список порожній, то викидувати
виняток ValueError(«List is empty»).
2. Видалення зі списку всіх значень X. Вхідні параметри: список і шукане значення для
видалення всіх входжень. Функція має змінювати наявний масив, видаляючи всі
входження шуканого значення.
3. Зробити функцію створення об'єкта користувача: функція приймає first_name,
last_name, birthday і має імітувати надсилання email-повідомлення. Щоб надіслати
email-повідомлення, використовуйте окрему функцію, яка друкуватиме текст
повідомлення в консоль про те, що зареєстрований новий користувач. Необхідно
протестувати цю функцію та реалізувати заглушку для надсилання пошти, щоб під час
тестування функція не виконувала жодного відправлення пошти (друк повідомлення в
консоль), а використовувалася заглушка (mock). Обов'язково перевірте факт виклику
функції надсилання електронної пошти.
"""

from unittest.mock import patch


def get_average(lst):
    if lst:
        return sum(lst) / len(lst)
    else:
        raise ValueError('List is empty')


def remove_all_x(lst, x):
    while x in lst:
        lst.remove(x)
    return lst


def send_email(first_name, last_name, birthday):
    print(f'New user {first_name} {last_name} registered')
    print(f'Email sent to {first_name} {last_name}, born on {birthday}')


def create_user(first_name, last_name, birthday):
    print(f'New user {first_name} {last_name} created')
    with patch('__main__.send_email') as mock_send_email:
        mock_send_email.return_value = 'Mock applied'
        send_email(first_name, last_name, birthday)


if __name__ == '__main__':
    print(get_average([1, 2, 3, 4]))
    print(remove_all_x([1, 2, 3, 4, 5, 3], 3))
    create_user('John', 'Smith', '1990-01-01')
