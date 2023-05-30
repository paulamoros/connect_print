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
    
    
def piece_informations():
    gfiles = cmdline("ls uploads/")
    
    gfiles_list = [str(i) for i in gfiles.split(b'\n')]
    gfiles_list.pop()
    
    
    if (len(gfiles_list) > 1):
        print("Multiple gcode files detected.")
        
    elif (len(gfiles_list) == 0):
        print("No gcode file detected.")
    
    else:
        
        gfile_name = "uploads/" + gfiles_list[0][2:-1]
        
        gfile = open(gfile_name, "r")
        
        commands = [line.strip() for line in gfile]
        
        informations = ""
        
        for j in commands:
            if(j == ""):
                break
            elif(j[0] == ";"):
                informations = informations + j[1:] + "\n"
                
    print(informations)
                
piece_informations()