import os

# Ports to monitor
ports_env = os.getenv('PORTS', '5432')
PORTS = [int(port.strip()) for port in ports_env.split(',')]

# log file path
# Get the current working directory
current_directory = os.getcwd()
LOG_PATH = os.getenv('LOG_PATH', '/root/streaming-analysis/logs/data.log')

