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

def printers_folders_update():
    
    #on collecte les ttyUSB connectés
    tty = cmdline("ls /dev/ttyUSB*")
    tty_list = [str(i) for i in tty.split(b'\n')]
    del tty_list[-1]
    print("Liste des imprimantes connectées: ",tty_list)
    
    #on vérifie maintenant les dossiers des imprimantes
    folders = cmdline("ls | grep d_imprimante")
    folders_list = []
    folders_list = [str(j) for j in folders.split(b'\n')]
    del folders_list[-1]
    print("Liste des dossiers d'imprimantes: ",folders_list)
    
    #on regarde enfin si le nombre d'imprimantes détectées correspond au nombre de dossiers d'imprimantes
    
    tty_number_list = []
    if len(folders_list) != len(tty_list):
        print("\nNombre de dossiers différent du nombre d'imprimantes détectées")
        #s'il y a une différence, on corrige cela
        
        
        #on créé d'abord des répertoires pour les tty en plus
        for i in tty_list:
            tty_number = i[13:-1]
            tty_number_list.append(int(tty_number))
            create_folder(int(tty_number))
            
        #on supprime ensuite les répertoires en trop (qui n'ont pas de tty associé)
        for i in folders_list:
            folder_number = int(i[14:-1])
            if folder_number not in tty_number_list:
                cmdline("sudo rm -dr d_imprimante"+str(folder_number))
        
        folders = cmdline("ls | grep d_imprimante")
        folders_list = []
        folders_list = [str(j) for j in folders.split(b'\n')]
        del folders_list[-1]
        print("\nNouvelle liste des dossiers d'imprimantes: ",folders_list)
        
    else:
        print("Nombre d'imprimantes branchées = Nombre de dossiers d'imprimantes")
        
    print("\nMise à jour du listing des imprimantes...\n")
    names = cmdline("lsusb | grep Future")
    names_list = []
    
    names_list = [str(i) for i in str(names).split("\\n")]
    del names_list[-1]
    #print(names_list)
    
    file = open("printers_infos.txt","w")
    listing_printers = []
    
    #print("\n\n\n"+ str(names_list))
    #print("\n\n\n"+ str(tty_list))
    #print("\n\n\n"+ str(folders_list))
    
    for i in range(len(names_list)):
        printer_links = [names_list[i],tty_list[i],folders_list[i]]
        listing_printers.append(printer_links)
    
    print(listing_printers)
    file.write(str(listing_printers))

def create_folder(p_number):
    
    # --- Folder creation --- #
    folder_name = "d_imprimante"+str(p_number)
    cmdline("mkdir "+folder_name)
    
    
    # --- Printer temperature files ---#
    cmdline("touch /var/www/html/"+folder_name+"/temp.txt")
    cmdline("sudo chmod 777 /var/www/html/"+folder_name+"/temp.txt")
    cmdline("sudo cp /var/www/html/gen_code/data.py /var/www/html/"+folder_name)
    cmdline("sudo mv /var/www/html/"+folder_name+"/data.py /var/www/html/"+folder_name+"/data"+str(p_number)+".py")
    cmdline("sudo chmod 777 /var/www/html/"+folder_name+"/data"+str(p_number)+".py")
    
    cmdline("sudo python ini_graph.py "+folder_name+" &")
    cmdline("sudo chmod 777 "+folder_name+"/graph.html")
    

    # --- Printer status files --- #
    cmdline("touch /var/www/html/"+folder_name+"/status.txt")
    cmdline("sudo chmod 777 /var/www/html/"+folder_name+"/status.txt")
    status = open(folder_name+"/status.txt","w")
    status.write("Free for printing")
    status.close()
    
    
    # --- Printer progression files --- #
    cmdline("touch /var/www/html/"+folder_name+"/timer.txt")
    cmdline("sudo chmod 777 /var/www/html/"+folder_name+"/timer.txt")
    timer_setup = open("d_imprimante"+str(p_number)+"/timer.txt", "a")
    timer_setup.write("Time left: Launch the printing to display the time left\nPercentage done: 0%")
    timer_setup.close()
    
    cmdline("sudo cp /var/www/html/gen_code/timer.py /var/www/html/"+folder_name)
    cmdline("sudo chmod 777 /var/www/html/d_imprimante"+str(p_number)+"/timer.py")
    cmdline("sudo mv /var/www/html/d_imprimante"+str(p_number)+"/timer.py /var/www/html/d_imprimante"+str(p_number)+"/timer"+str(p_number)+".py")    
    
    
    # --- Web pages files --- #
    cmdline("sudo cp /var/www/html/gen_code/imprimante.php /var/www/html/d_imprimante"+str(p_number))
    
    cmdline("sudo cp /var/www/html/gen_code/interface.php /var/www/html/d_imprimante"+str(p_number))
    cmdline("sudo sed -i 's/#IMP_NB#/"+str(p_number)+"/g' /var/www/html/d_imprimante"+str(p_number)+"/interface.php")
    
    cmdline("sudo cp /var/www/html/gen_code/piece_information.py /var/www/html/d_imprimante"+str(p_number))
    
    
    # --- Printing commands files --- #
    cmdline("sudo cp /var/www/html/gen_code/print.py /var/www/html/d_imprimante"+str(p_number))
    cmdline("sudo mv /var/www/html/d_imprimante"+str(p_number)+"/print.py /var/www/html/d_imprimante"+str(p_number)+"/print"+str(p_number)+".py")
    
    cmdline("sudo cp /var/www/html/gen_code/control_printer.py /var/www/html/d_imprimante"+str(p_number))
    cmdline("sudo chmod 777 /var/www/html/d_imprimante"+str(p_number)+"/control_printer.py")
    
    cmdline("sudo mkdir /var/www/html/d_imprimante"+str(p_number)+"/uploads/")
    cmdline("sudo chmod 777 /var/www/html/d_imprimante"+str(p_number)+"/uploads/")
    
    # --- Recap files --- #
    cmdline("sudo touch /var/www/html/recap.txt")
    cmdline("sudo chmod 777 /var/www/html/recap.txt")
    
    print("Folder n°"+str(p_number)+" created")
    


def force_reset():
    folder_nb = int(cmdline("ls | grep d_imprimante | wc -l"))
    for i in range (folder_nb):
        print("sudo rm -dr d_imprimante"+str(i))
        cmdline("sudo rm -dr d_imprimante"+str(i))
    cmdline("sudo rm recap.txt")
    printers_folders_update()
    
    
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
   
   
force_reset()
index_update()