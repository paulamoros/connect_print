import signal
import time
from multiprocessing import Value

running = Value('i', 1)

def stop_process(signum, frame):
    print("Arrêt du processus")
    running.value = 0
    
