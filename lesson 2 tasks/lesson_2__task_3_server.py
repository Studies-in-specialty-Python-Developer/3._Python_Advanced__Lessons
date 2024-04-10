""" Урок 2, завдання 3
Створіть UNIX-сокет, який приймає повідомлення з двома числами, що розділені комою. Сервер
має конвертувати рядкове повідомлення у два числа й обчислювати його суму. Після успішного
обчислення повертати відповідь клієнту.
"""

import socket
import os

SOCKET_FILE = 'unix_socket.sock'

if os.path.exists(SOCKET_FILE):
    os.remove(SOCKET_FILE)

sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
sock.bind(SOCKET_FILE)
sock.listen()

while True:
    data, addr = sock.recvfrom(1024)
    print(f'New connection from {addr}')
    data = data.decode().split(',')
    numbers = list(map(int, data))
    print(f'Received numbers: {numbers[0]}, {numbers[1]}')
    result = numbers[0] + numbers[1]
    sock.sendto(str(result).encode(), addr)
    print(f'Sent Sum = {result} to:', addr)
    print()
