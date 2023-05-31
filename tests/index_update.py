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
    
    
def index_update():
    
    cmdline("sudo rm /var/www/html/index.php")
    printers_options = ""
    option = ""
    redirection = ""
    redirections = ""
    
    printers_infos = open("/var/www/html/printers_infos.txt","r")
    printers_list = eval(printers_infos.readlines()[0])
    
    for i in range(len(printers_list)):
        option = "<option value=\""+str(i)+"\">Printer "+str(i)+ "</option>\n"
        printers_options = printers_options + option
        
        redirection = "'"+str(i)+"' => 'd_imprimante"+str(i)+"/imprimante.php',\n"
        redirections = redirections + redirection
    
    
    index = open('/var/www/html/gen_code/index.php', 'r')
    index_lines = index.readlines()
    index.close()

    new_lines = ""
    new_index = open('/var/www/html/index.php', 'a')    
    
    for i in range(len(index_lines)):
        
        if index_lines[i] == "#PRINTERS_OPTIONS#\n":
            new_index.write(new_lines)
            new_lines = ""
            new_index.write(printers_options)
        
        elif index_lines[i] == "#REDIRECTIONS#\n":
            new_index.write(new_lines)
            new_lines = ""
            new_index.write(redirections)
            
        
        else:
            new_lines = new_lines + index_lines[i]
         
             
    new_index.write(new_lines)
    new_index.close()



   

index_update()