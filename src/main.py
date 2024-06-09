import asyncio
import network.listener as listener
from log_monitor.monitor import monitor_file
from multiprocessing import Process

def monitorlogfile():
    asyncio.run(monitor_file('incoming_data.log'))

def networklistner():
    asyncio.run(listener.main())

    # await task2
if __name__ == "__main__":
    p1 = Process(target = networklistner)
    p1.start()
    p2 = Process(target = monitorlogfile)
    p2.start()
    p1.join()
    p2.join()