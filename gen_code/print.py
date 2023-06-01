#!/usr/bin/env python

import time
import sys
import serial
import os
import signal
from datetime import datetime
from subprocess import PIPE, Popen
import fcntl

lock_file = '/var/www/html/locks/locker_'+sys.argv[0][:-3]+'.lock'
print(lock_file)

try:
    file_handle = open(lock_file, "w")
    fcntl.flock(file_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)

except IOError:
    print("The print script is already running.")
    sys.exit(0)

def cmdline(command):
        process = Popen(
                args=command,
                stdout=PIPE,
                shell=True
        )
        return process.communicate()[0]

pause = False
stop = False


# Signals handling for the commands of printer pausing and stopping 

def handle_signal_stop(signal, frame):
    print("Impression stopped")
    global stop
    status_update("Printing stopped, please clean the printer to start a new impression.")
    stop = True
    
    
def handle_signal_pause(signal, frame):
    global pause
    if(pause == True):
        pause = False
        print("Impression resumed")
        status_update("Printing")
    else:
        pause = True
        print("Impression paused")
        status_update("Printing paused")
    
    
signal.signal(signal.SIGUSR1, handle_signal_stop)
signal.signal(signal.SIGUSR2, handle_signal_pause)

#fin de la partie de gestion des pauses / arrêts

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
    print("Status updated: "+new_status)
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

    try:
        # we test if the printer is cleaned
        
        status_file = open("status.txt", "r")
        status = status_file.read()
        print (status)
        if (status == "Printing stopped, please clean the printer to start a new impression."):
            status_update("Can't start a new impression while te printer is not cleaned.")
            sys.exit()
            
        status_file.close()
        
        commands = commands_maker()
        status_update("Printing")
        
        print(commands[0:10])
        
        x=0
        
        while(x != len(commands)):
            
            #check de la réception des signaux d'arrêt ou de pause
            
            if stop == True:
                ser.write('G92 \r\n'.encode())
                while True:
                    line = ser.readline()
                    if (line[:2] == b'ok'):
                        break
                sys.exit()
                
            while (pause == True):
                time.sleep(2)
                if stop == True:
                    ser.write('G92 \r\n'.encode())
                    sys.exit()
            
            
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
            
            if x%10 == 0:
                # timer update every 10 gcode commande
                percentage_done = (x/len(commands))*100
                timer = open("timer.txt","r")
                timer_lines = timer.readlines()
                timer.close()
                timer = open("timer.txt","w")
                if len(timer_lines) == 2:
                    timer_lines[1] = "Percentage done: "+str("{:.2f}".format(percentage_done))+"%"
                    new_text = timer_lines[0]+timer_lines[1]
                    timer.write(new_text)
            
                timer.close()
                
                #then, temperature gathering every 10 gcode commands
                
                print("temperature command sending")
                ser.write(temp_command)
                while True:
                    line = ser.readline()
                    print (line)
                    
                    if (line[:5] == b'ok T:' or line[:1]==b'X'):
                        break
                    
                
                if(line[:5] == b'ok T:'):
                    temp_infos = str(line).split(" ")
                    temp = temp_infos[1][2:]
                    abs_time = time.time()
                    line = "["+temp+" , "+str(abs_time)+"]"
                    print(line)
                    
                    temp_file = open('temp.txt', 'a')
                    temp_file.write(str(line)+"\n")
                    temp_file.close()
                    print("temperature gathering finished")
                
                
        
        time.sleep(3)
        status_update("Print finished")
    
    # then whatever the error is, we need to free the lock
    finally:
        fcntl.flock(file_handle, fcntl.LOCK_UN)
        file_handle.close()

printing()


