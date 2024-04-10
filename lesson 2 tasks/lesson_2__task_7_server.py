""" Урок 2, завдання 7
Створити простий чат на основі протоколу TCP, який дасть змогу під'єднуватися кільком клієнтам
та обмінюватися повідомленнями.
"""

import socket
import threading

HOST_IP = '127.0.0.1'
HOST_PORT = 4321


# Processing incoming messages from the client
def handle_client(client_socket, address):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Received message from {address}: {data.decode()}")
        for client in clients:
            if client != client_socket:
                client.send(data)
    client_socket.close()


# Creating socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen(5)

print("Server started. Waiting for connections...")
clients = []
while True:
    client_sock, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")
    clients.append(client_sock)
    client_thread = threading.Thread(target=handle_client, args=(client_sock, addr))
    client_thread.start()
