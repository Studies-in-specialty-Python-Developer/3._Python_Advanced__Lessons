""" Урок 2, завдання 2
Створіть UDP-сервер, який очікує на повідомлення про нові пристрої в мережі. Він приймає
повідомлення певного формату, де буде ідентифікатор пристрою, і друкує нові під'єднання в
консоль. Створіть UDP-клієнта, який надсилатиме унікальний ідентифікатор пристрою на сервер,
повідомляючи про свою присутність.
"""

import random
import socket

SOCKET_IP = '127.0.0.1'
SOCKET_PORT = 4321

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
uuid = str(random.randint(1000000, 10000000))
sock.sendto(uuid.encode(), (SOCKET_IP, SOCKET_PORT))
print('Sent UUID:', uuid)
sock.close()
