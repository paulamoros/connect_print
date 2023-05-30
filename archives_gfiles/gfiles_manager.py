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

def save_gfile(p_number, name):
    cmdline("sudo cp /var/www/html/d_imprimante"+str(p_number)+"/"+name+" /var/www/html/archives_gfiles")
    date = str(cmdline("date +'%x'"))
    date = "d"+date[2:4]+"m"+date[5:7]+"y"+date[8:12]
    time = str(cmdline("date +'%X'"))
    time = "h"+time[2:4]+"m"+time[5:7]+"s"+time[8:10]
    new_name = ""
    new_name = date+"_"+time+"_printer"+str(p_number)+"_"+name
    #print (new_name)
    cmdline("sudo mv /var/www/html/archives_gfiles/"+name+" /var/www/html/archives_gfiles/"+new_name)
    
def clear_saves():
    cmdline("sudo rm /var/www/html/archives_gfiles/*")


#save_gfile(1,"imprimante.php")
#clear_saves()