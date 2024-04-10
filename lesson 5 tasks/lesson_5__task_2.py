""" Урок 5, завдання 2
Розробіть сокет-сервер на основі бібліотеки asyncio.
"""

import asyncio

HOST_IP = '127.0.0.1'
HOST_PORT = 4321


async def handle_client(reader, writer):
    data = await reader.read(1024)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(f'Received {message} from {addr}')
    print(f'Send: {message}')
    writer.write(data)
    await writer.drain()
    print('Closing the connection')
    writer.close()


async def main():
    server = await asyncio.start_server(
        handle_client, HOST_IP, HOST_PORT)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()


asyncio.run(main())
