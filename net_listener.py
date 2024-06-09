#!/usr/bin/env python3

import os
import asyncio
import socket
import logging

# Define the file to which data will be appended
file_path = 'incoming_data.log'

# Get ports from environment variable
ports_env = os.getenv('PORTS', '514,515,516')
ports = [int(port.strip()) for port in ports_env.split(',')]

# Asynchronous function to handle incoming TCP connections
async def handle_tcp_client(reader, writer):
    while True:
        data = await reader.read(100)
        if not data:
            break
        try:
            decoded_data = data.decode('utf-8')
            append_to_file(decoded_data)
        except UnicodeDecodeError:
            # Handle corrupted data
            print("Corrupted TCP data received and ignored")
    writer.close()
    await writer.wait_closed()

# Asynchronous function to handle incoming UDP data
async def handle_udp_server(port):
    loop = asyncio.get_running_loop()
    udp_transport, udp_protocol = await loop.create_datagram_endpoint(
        lambda: UDPServerProtocol(),
        local_addr=('0.0.0.0', port)
    )

class UDPServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        try:
            decoded_data = data.decode('utf-8')
            append_to_file(decoded_data)
        except UnicodeDecodeError:
            # Handle corrupted data
            print("Corrupted UDP data received and ignored")

def append_to_file(data):
    with open(file_path, 'a') as file:
        file.write(data + '\n')

async def main():
    tasks = []

    # Create TCP servers for each port
    for port in ports:
        print(f'UDP: Listening on port {port}')
        server = await asyncio.start_server(handle_tcp_client, '0.0.0.0', port)
        tasks.append(server.serve_forever())

    # Create UDP servers for each port
    for port in ports:
        print(f'UDP: Listening on port {port}')
        tasks.append(handle_udp_server(port))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())