#This code kills the printing process on the Raspberry, can only be used by an administrator

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
    
    
    
def print_killer():
    folder_name = cmdline("current_dir=$(pwd); echo \"${current_dir##*/}\"").decode('utf-8')
    folder_number = folder_name[12:]
    
    process_name = "print"+folder_number
    
    process = cmdline("ps aux | grep www-data | grep "+ process_name)
    
    #process = str(process)
    
    process_table = process.split(" ")
    process_infos = []
    
    for i in range(0,len(process_table)):
        if process_table[i] != "":
            process_infos.append(process_table[i])
            
    #print(process_infos)
    
    pid = process_infos[1]
    
    cmdline("sudo kill 3 "+pid)
    
    return pid


print_killer()
    
    
