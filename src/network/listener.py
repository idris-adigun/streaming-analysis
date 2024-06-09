import os
import asyncio
import signal
import sys
import json
import time
import config.logger as logger

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
            logger.logInfo('Deconding data...')
            decoded_data = data.decode('utf-8')
            logger.logInfo('Data decoded')
            append_to_file(decoded_data)
        except UnicodeDecodeError:
            # Handle corrupted data
            logger.logInfo('Corrupted TCP data received and ignored')
    writer.close()
    await writer.wait_closed()

# Asynchronous function to handle incoming UDP data
async def handle_udp_server(port):
    loop = asyncio.get_running_loop()
    udp_transport, udp_protocol = await loop.create_datagram_endpoint(
        lambda: UDPServerProtocol(),
        local_addr=('0.0.0.0', port)
    )
    return udp_transport

class UDPServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        try:
            decoded_data = data.decode('utf-8')
            append_to_file(decoded_data)
        except UnicodeDecodeError:
            # Handle corrupted data
            logger.logInfo('Corrupted UDP data received and ignored')

def append_to_file(data):
    timestamp = int(time.time())
    message_dict = {"timestamp": timestamp, "message": data}
    with open(file_path, 'a') as file:
        logger.logInfo('Appending data to file')
        json.dump(message_dict, file)
        file.write('\n')  # Add newline for readability

async def main():
    tasks = []
    servers = []

    # Create TCP servers for each port
    for port in ports:
        logger.logInfo(f'TCP: Listening on port - {port}')
        server = await asyncio.start_server(handle_tcp_client, '0.0.0.0', port)
        servers.append(server)
        tasks.append(asyncio.create_task(server.serve_forever()))

    # Create UDP servers for each port
    for port in ports:
        logger.logInfo(f'UDP: Listening on port - {port}')
        udp_transport = await handle_udp_server(port)
        servers.append(udp_transport)
    
    # Add graceful shutdown handling
    async def shutdown(signal, loop):
        logger.logError(f"Received exit signal {signal.name}...")
        print(f"Received exit signal {signal.name}...")
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        for server in servers:
            if isinstance(server, asyncio.base_events.Server):
                server.close()
                await server.wait_closed()
            else:
                server.close()
        loop.stop()

    loop = asyncio.get_running_loop()

    if sys.platform != "win32":
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(shutdown(s, loop)))
    else:
        # Windows does not support add_signal_handler, use another method
        loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(shutdown(signal.SIGINT, loop)))

    await asyncio.gather(*tasks)