#!/usr/bin/env python

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
    
temp_command = 'M105\n'.encode()

ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 250000,
        )

    
def send_temp_check():
    
    
    
    ser.write(temp_command)
    
    while True:
        line = ser.readline()
        print (line)
        print(line[5:])
        if (line[:2] == b'ok' or line[:1]==b'X'):
            break
    
    
    temp_infos = str(line).split(" ")
    temp = temp_infos[1][2:]
    if(temp_infos[1][:2] == 'T:'):
        abs_time = time.time()
        line = "["+temp+" , "+str(abs_time)+"]"
        print(line)
        
        temp_file = open('temp.txt', 'a')
        temp_file.write(str(line)+"\n")
        temp_file.close()


while True:
    send_temp_check()
    time.sleep(1)