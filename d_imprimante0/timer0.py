import time
import sys
import serial
import os
import signal
from datetime import datetime
from subprocess import PIPE, Popen
import fcntl


#We fist create a lock that will be used to make sure we don't duplicate the execution of this script

lock_file = '/var/www/html/locks/locker_'+sys.argv[0][:-3]+'.lock'
print(lock_file)

try:
    file_handle = open(lock_file, "w")
    fcntl.flock(file_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)

except IOError:
    print("The timer script is already running.")
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


#The signals handlers detects when the control_printer.py script sends a signal if the user clicks a "pause/resume" or "stop" button

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
    #Just a function to write new data in timer.txt
    
    timer = open("timer.txt", "r")
    lines = timer.readlines()
    print(lines)
    timer.close()
    
    timer = open("timer.txt", "w")
    lines[0] = new_status
    timer.write(lines[0]+lines[1])
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
            print("No duration information found.")
    
    return duration


def total_sec(time_string):
    #This function converts the time duration string detected in the g-file code into an int number of seconds
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
    
    #We add an offset to the total printing time, due to the calibration and heating of the printer, that lasts about 2min
    total_sec = total_sec + 220
    
    return(total_sec)



def format_duration(sec):
    #This function formats the number of seconds in HH:MM:SS
    hours = sec//3600
    minutes = (sec % 3600) // 60
    seconds = sec % 60
    formated_duration = "{:02d}:{:02d}:{:02d}".format(hours,minutes,seconds)
    return formated_duration


def timer(sec_nb):
    #This functions runs the timer and updates the timer.txt file to display the timer on the website
    
    try:
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
            
            timer_update("Time left: "+str(formated_time_left)+"\n")
            
            time.sleep(1)
        
        timer_update("Printing almost finished\n")
        
    # then whatever the error is, we need to free the lock
    finally:
        fcntl.flock(file_handle, fcntl.LOCK_UN)
        file_handle.close()
        

time_string = time_finder()

total_seconds = total_sec(time_string)

timer(total_seconds)

fcntl.flock(file_handle, fcntl.LOCK_UN)
file_handle.close()