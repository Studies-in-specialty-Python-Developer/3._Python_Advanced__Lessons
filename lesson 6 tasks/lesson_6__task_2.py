""" Урок 6, завдання 2
Створіть три функції, одна з яких читає файл на диску із заданим ім'ям та перевіряє наявність рядка
«Wow!». Якщо файлу немає, то засипає на 5 секунд, а потім знову продовжує пошук по файлу. Якщо файл
є, то відкриває його і шукає рядок «Wow!». За наявності цього рядка закриває файл і генерує подію, а інша
функція чекає на цю подію і у разі її виникнення виконує видалення цього файлу. Якщо рядки «Wow!» не
було знайдено у файлі, то засипати на 5 секунд. Створіть файл руками та перевірте виконання програми.
"""

import threading
import os
import time

FILE_NAME = 'lesson_6__task_2_test.txt'


def check_file(file_found_event):
    while True:
        files = list(filter(os.path.isfile, os.listdir(os.curdir)))
        if FILE_NAME in files:
            with open(FILE_NAME, 'r') as file:
                if 'Wow!' in file.read():
                    file_found_event.set()
                    return
                else:
                    print('"Wow!" in file not found, waiting 5 sec.')
                    time.sleep(5)
        else:
            print('File not found, waiting 5 sec.')
            time.sleep(5)


def delete_file(file_found_event):
    print('Wait for file')
    file_found_event.wait()
    file_found_event.clear()
    os.remove(FILE_NAME)
    print('File found and deleted!')


file_found = threading.Event()

check_file_task = threading.Thread(target=check_file, args=(file_found,))
delete_file_task = threading.Thread(target=delete_file, args=(file_found,))

check_file_task.start()
delete_file_task.start()

check_file_task.join()
delete_file_task.join()
