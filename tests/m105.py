import time
import sys
import serial
import os
import signal
from datetime import datetime
from subprocess import PIPE, Popen


def cmdline(command):
        process = Popen(
                args=command,
                stdout=PIPE,
                shell=True
        )
        return process.communicate()[0]
    
    
ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 250000,
        )

command = 'M105\n'.encode()
print(command)

while True:
    ser.write(command)
    line = ser.readline()
    print(line)
    time.sleep(0.1)
    print("new_temp")
    