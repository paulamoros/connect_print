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
    
    
    
def pid_finder():
    folder_name = cmdline("current_dir=$(pwd); echo \"${current_dir##*/}\"").decode('utf-8')
    folder_number = folder_name[12:]
    process_name = "print"+folder_number
    
    process = cmdline("ps aux | grep "+ process_name)
    
    print(process)
    return process


pid_finder()
    
    
