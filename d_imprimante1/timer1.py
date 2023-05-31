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
    
    
pause = False
stop = False


def handle_signal_stop(signal, frame):
    print("Timer stopped")
    global stop
    timer_update("Printing stopped.")
    stop = True
    
    
def handle_signal_pause(signal, frame):
    global pause
    if(pause == True):
        pause = False
        print("Timer resumed")
    elif(pause == False):
        pause = True
        print("Timer paused")
        
signal.signal(signal.SIGUSR1, handle_signal_stop)
signal.signal(signal.SIGUSR2, handle_signal_pause)
        

def timer_update(new_status):
    timer = open("timer.txt", "w")
    timer.write(new_status)
    timer.close()


def time_finder():
    
    gfiles = cmdline("ls uploads/")
    
    gfiles_list = [str(i) for i in gfiles.split(b'\n')]
    gfiles_list.pop()
    
    
    if (len(gfiles_list) > 1):
        print("Multiple gcode files detected.")
        
    elif (len(gfiles_list) == 0):
        print("No gcode file detected.")
    
    else:
        
        duration_found = False
        duration = ""
        
        gfile_name = "uploads/" + gfiles_list[0][2:-1]
        gfile = open(gfile_name, "r")
        text = gfile.read()
        
        lines = [str(i) for i in text.split('\n')]
        
        for i in lines[:10]:
            if i[:17] == ";Print duration: ":
                duration = i[17:]
                print (duration)
                duration_found = True
            
        if duration_found == False:
            print("no duration information found.")
    
    return duration


def total_sec(time_string):
    
    total_sec = 0
    
    time_sep = [str(i) for i in time_string.split(' ')]
    
    nb_units = len(time_sep)/2
        
    for i in range(int(nb_units)+1):
        
        if i%2 == 0:
            value = float(time_sep[i])
            
        else:
            unit = time_sep[i]
            if unit == "sec":
                total_sec = total_sec + value
            elif unit == "min":
                total_sec = total_sec + (value*60)
            elif unit == "hr":
                total_sec = total_sec + (value*3600)
    
    return(total_sec)



def format_duration(sec):
    hours = sec//3600
    minutes = (sec % 3600) // 60
    seconds = sec % 60
    formated_duration = "{:02d}:{:02d}:{:02d}".format(hours,minutes,seconds)
    return formated_duration


def timer(sec_nb):
    
    start_time = time.time()
    
    end_time = start_time + sec_nb
    
    time_left = sec_nb
    
    while(end_time > time.time()):
        
        if stop == True:
            timer_update("Printing stopped")
            break
            print("exit check")
            
        elif pause == True:
        
            timer_update(str(formated_time_left+" (Paused)"))
            while pause == True:
                end_time = end_time + 1.0
                time.sleep(1)
        
        time_left = int(round(end_time)) - int(round(time.time()))
        formated_time_left = format_duration(time_left)
        
        timer_update(str(formated_time_left))
        
        time.sleep(1)
    

time_string = time_finder()

total_seconds = total_sec(time_string)

timer(total_seconds)
