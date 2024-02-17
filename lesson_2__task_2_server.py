""" Урок 2, завдання 2
Створіть UDP-сервер, який очікує на повідомлення про нові пристрої в мережі. Він приймає
повідомлення певного формату, де буде ідентифікатор пристрою, і друкує нові під'єднання в
консоль. Створіть UDP-клієнта, який надсилатиме унікальний ідентифікатор пристрою на сервер,
повідомляючи про свою присутність.
"""

import socket

SOCKET_IP = '127.0.0.1'
SOCKET_PORT = 4321

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SOCKET_IP, SOCKET_PORT))
while True:
    data, addr = sock.recvfrom(1024)
    print(f'New connection from {addr}')
    print(f'Received UUID: {data.decode()}')
    print()
