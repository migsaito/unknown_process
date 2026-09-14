#!/usr/bin/env python3
import ctypes
import time
import os
import signal
import sys
import multiprocessing

# Ignora SIGINT (Ctrl+C) e SIGTERM (kill comum). 
# O processo só aceitará finalização via SIGKILL (kill -9).
signal.signal(signal.SIGINT, signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)

def renomear_processo(nome="miguel"):
    try:
        libc = ctypes.CDLL('libc.so.6')
        libc.prctl(15, nome.encode('utf-8') + b'\0', 0, 0, 0)
    except Exception:
        pass

def carga_cpu(target_ratio=0.20, interval=0.05):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    renomear_processo("miguel")
    
    busy_time = interval * target_ratio
    sleep_time = interval * (1.0 - target_ratio)
    
    while True:
        start = time.perf_counter()
        while (time.perf_counter() - start) < busy_time:
            _ = 3.14159 ** 2.71828
        time.sleep(sleep_time)

if __name__ == '__main__':
    renomear_processo("miguel")

    # Aloca exatamente 3 GB (3072 MB) de memória física real e silenciosa
    target_ram_mb = 3072
    memory_block = bytearray(b'x' * (target_ram_mb * 1024 * 1024))

    # Cria subprocessos para distribuir os 20% de uso por todas as threads da CPU
    num_cpus = os.cpu_count() or 1
    workers = []
    
    for _ in range(num_cpus):
        p = multiprocessing.Process(target=carga_cpu, args=(0.20, 0.05))
        p.daemon = True
        p.start()
        workers.append(p)

    # Mantém o processo principal travado e ativo
    try:
        while True:
            time.sleep(3600)
    except Exception:
        pass
