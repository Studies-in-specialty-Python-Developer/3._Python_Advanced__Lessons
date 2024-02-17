""" Урок 2, завдання 2
Створіть UNIX-сокет, який приймає повідомлення з двома числами, що розділені комою. Сервер
має конвертувати рядкове повідомлення у два числа й обчислювати його суму. Після успішного
обчислення повертати відповідь клієнту.
"""

import random
import socket
import os

SOCKET_FILE = 'unix_socket.sock'

if not os.path.exists(SOCKET_FILE):
    print('File does not exist')
    exit()

sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
sock.connect(SOCKET_FILE)

numbers = str(random.randint(0, 10)) + ', ' + str(random.randint(0, 10))
sock.sendall(numbers.encode())
print('Sent numbers:', numbers)
summ = sock.recv(1024).decode()
print('Received sum =', summ)
sock.close()
