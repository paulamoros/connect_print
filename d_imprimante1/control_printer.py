#!/usr/bin/env python

#This scripts uses the signals to allow the printer command asynchronously

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
    
    
    
def pid_finder(script_name):
    
    #To send signals with SIGUSR1 and SIGUSR2, we need to find the pid of print.py
    
    folder_name = cmdline("current_dir=$(pwd); echo \"${current_dir##*/}\"").decode('utf-8')
    folder_number = folder_name[12:]
    
    process_name = script_name + folder_number
    print ("Process name: ",process_name)
    process = cmdline("ps aux | grep "+ process_name).decode('utf-8')
    print ("Process: ", process)
    
    process_table = process.split(" ")
    process_infos = []
    
    for i in range(0,len(process_table)):
        if process_table[i] != "":
            process_infos.append(process_table[i])
            
    pid = process_infos[1]
    print ("PID: ", pid)
    return pid
    
    
#The os library have a kill method to send signals to other processes

def send_stop(pid):
    os.kill(pid, signal.SIGUSR1)
    
def send_pause(pid):
    os.kill(pid, signal.SIGUSR2)
    
def pause_timer(pid):
    os.kill(pid, signal.SIGUSR2)

def stop_timer(pid):
    os.kill(pid, signal.SIGUSR1)
    
    
def printer_cleaned():
    status_file = open("status.txt", "w")
    status_file.write("Free to start")


#We use arguments in entry of the script to differentiate the commands
    
if (sys.argv[1] == "stop"):
    print(pid_finder("print"))
    send_stop(int(pid_finder("print")))
    print(pid_finder("timer"))
    stop_timer(int(pid_finder("timer")))
    
    
elif (sys.argv[1] == "pause"):
    print(pid_finder("print"))
    send_pause(int(pid_finder("print")))
    print(pid_finder("timer"))
    pause_timer(int(pid_finder("timer")))
    

elif (sys.argv[1] == "clean"):
    printer_cleaned()
    
    
    

