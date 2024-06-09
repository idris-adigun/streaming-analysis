import os
import asyncio
import network.listener as listener
from log_monitor.monitor import monitor_file
from multiprocessing import Process
import config.env as env

log_file_path = env.LOG_PATH

def monitorlogfile():
    asyncio.run(monitor_file(log_file_path))

def networklistner():
    asyncio.run(listener.main())
    
if __name__ == "__main__":
    listnening_process = Process(target = networklistner)
    listnening_process.start()
    monitoring_process = Process(target = monitorlogfile)
    monitoring_process.start()
    listnening_process.join()
    monitoring_process.join()