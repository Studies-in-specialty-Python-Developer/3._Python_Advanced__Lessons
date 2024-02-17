""" Урок 2, завдання 7
Створити простий чат на основі протоколу TCP, який дасть змогу під'єднуватися кільком клієнтам
та обмінюватися повідомленнями.
"""

import socket
import threading

HOST_IP = '127.0.0.1'
HOST_PORT = 4321


# Processing incoming messages from the server
def receive_messages(client_sock):
    while True:
        try:
            data = client_sock.recv(1024)
            if not data:
                break
            print()
            print(data.decode())
        except Exception as e:
            print(f"Error receiving message: {e}")
            break


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST_IP, HOST_PORT))
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()
while True:
    message = input('Input message: ')
    if message.lower() == 'exit':
        break
    client_socket.send(message.encode())

client_socket.close()
