import asyncio
import network.listener as listener
from log_monitor.monitor import monitor_file
from multiprocessing import Process
import config.env as env

log_file_path = env.LOG_PATH

def monitor_logfile():
    asyncio.run(monitor_file(log_file_path))

def network_listener():
    asyncio.run(listener.main())
    
if __name__ == "__main__":
    listening_process = Process(target = network_listener)
    listening_process.start()
    monitoring_process = Process(target = monitor_logfile)
    monitoring_process.start()
    listening_process.join()
    monitoring_process.join()