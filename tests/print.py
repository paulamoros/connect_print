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



def tty_lookup():
    printer_infos_file = open("../printers_infos.txt","r")
    printer_infos = eval(printer_infos_file.read())
    
    folder_name = cmdline("current_dir=$(pwd); echo \"${current_dir##*/}\"").decode('utf-8')

    tty = ""
    
    for i in printer_infos:
        if (i[2][2:-1] == folder_name[:-1]):
            tty = i[1][2:-1]
        
    if (tty == ""):
        print("No printer linked to this folder, an architecture problem happened.")
        
    return tty
    
   
ser = serial.Serial(
        port=tty_lookup(),
        baudrate = 250000,
        )


gfiles = cmdline("ls uploads/")
gfiles_list = [str(i) for i in gfiles.split(b'\n')]
gfiles_list.pop()

temp_command = 'M105\n'.encode()


def one_file_check():
    
    val = 1
    if (len(gfiles_list) > 1):
        print("Multiple gcode files detected.")
        val = 1
        
    elif (len(gfiles_list) == 0):
        print("No gcode file detected.")
        val = 1
        
    else:
        print("One file correctly detected.\n")
        val = 0
        
    return val
    
    
def status_update(new_status):
    status = open("status.txt","w")
    status.write(new_status)
    status.close()
    
    

def commands_maker():
    
    commands = []
    if(one_file_check() == 0):
        gfile_name = "uploads/" + gfiles_list[0][2:-1]
        
        gfile = open(gfile_name, "r")
        
        file_lines = [line.strip() for line in gfile]
        commands = []
        
        for i in range(0,len(file_lines)):
            if (file_lines[i]!="" and file_lines[i][0] != ";"):
                no_comment = ""
                for j in file_lines[i]:
                    if j == ";":
                        break
                    no_comment = no_comment + j
                     
                no_comment = no_comment + "\r\n"
                commands.append(no_comment)
                
    else:
        print("Not only one file detected, please make sure there is only one gfile in uploads/.")
        
    return commands


def printing():

    commands = commands_maker()
    status_update("Printing")
    
    print(commands[0:10])
    
    x=0
    
    while(x != len(commands)):
        print(commands[x])
        command = commands[x]
        
        ser.write(str.encode(command))
        while True:
            line = ser.readline()
            print (line)
            if (line[:2] == b'ok' or line[:1]==b'X'):
                
                break
            
            elif (line[1:3] == b'T:'):
                
                temp_infos = str(line).split(" ")
                temp = temp_infos[1][2:]
                abs_time = time.time()
                line = "["+temp+" , "+str(abs_time)+"]"
                print(line)
                
                temp_file = open('temp.txt', 'a')
                temp_file.write(str(line)+"\n")
                temp_file.close()
                
        x = x+1
   
    
    time.sleep(3)
    status_update("Print finished")
    

printing()