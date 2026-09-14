import ctypes
import time
import os
import signal
import sys
import multiprocessing

signal.signal(signal.SIGINT, signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)

def set_proc_name(name="miguel"):
    try:
        libc = ctypes.CDLL('libc.so.6')
        libc.prctl(15, name.encode('utf-8') + b'\0', 0, 0, 0)
    except Exception:
        pass

def cpu_workload(target_ratio=0.20, interval=0.05):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    set_proc_name("miguel")
    
    busy_time = interval * target_ratio
    sleep_time = interval * (1.0 - target_ratio)
    
    while True:
        start = time.perf_counter()
        while (time.perf_counter() - start) < busy_time:
            _ = 3.14159 ** 2.71828
        time.sleep(sleep_time)

if __name__ == '__main__':
    set_proc_name("miguel")

    target_ram_mb = 3072
    memory_block = bytearray(b'x' * (target_ram_mb * 1024 * 1024))

    num_cpus = os.cpu_count() or 1
    workers = []
    
    for _ in range(num_cpus):
        p = multiprocessing.Process(target=cpu_workload, args=(0.20, 0.05))
        p.daemon = True
        p.start()
        workers.append(p)

    try:
        while True:
            time.sleep(3600)
    except Exception:
        pass
