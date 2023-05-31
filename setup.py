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
    
    folder_name = "d_imprimante"+str(p_number)
    cmdline("mkdir "+folder_name)
    
    cmdline("touch /var/www/html/"+folder_name+"/temp.txt")
    cmdline("sudo chmod 777 /var/www/html/"+folder_name+"/temp.txt")
    cmdline("touch /var/www/html/"+folder_name+"/status.txt")
    cmdline("sudo chmod 777 /var/www/html/"+folder_name+"/status.txt")
    
    cmdline("touch /var/www/html/"+folder_name+"/timer.txt")
    cmdline("sudo chmod 777 /var/www/html/"+folder_name+"/timer.txt")
    timer_setup = open("d_imprimante"+str(p_number)+"/timer.txt", "a")
    timer_setup.write("Time left: Launch the printing to display the time left\nPercentage done: 0%")
    timer_setup.close()
    
    cmdline("sudo cp /var/www/html/gen_code/imprimante.php /var/www/html/d_imprimante"+str(p_number))
    cmdline("sudo cp /var/www/html/gen_code/interface.php /var/www/html/d_imprimante"+str(p_number))
    cmdline("sudo cp /var/www/html/gen_code/piece_information.py /var/www/html/d_imprimante"+str(p_number))
    
    cmdline("sudo cp /var/www/html/gen_code/timer.py /var/www/html/d_imprimante"+str(p_number))
    cmdline("sudo chmod 777 /var/www/html/d_imprimante"+str(p_number)+"/timer.py")
    cmdline("sudo mv /var/www/html/d_imprimante"+str(p_number)+"/timer.py /var/www/html/d_imprimante"+str(p_number)+"/timer"+str(p_number)+".py")    
    
    cmdline("sudo cp /var/www/html/gen_code/print.py /var/www/html/d_imprimante"+str(p_number))
    cmdline("sudo mv /var/www/html/d_imprimante"+str(p_number)+"/print.py /var/www/html/d_imprimante"+str(p_number)+"/print"+str(p_number)+".py")
    
    cmdline("sudo cp /var/www/html/gen_code/control_printer.py /var/www/html/d_imprimante"+str(p_number))
    cmdline("sudo chmod 777 /var/www/html/d_imprimante"+str(p_number)+"/control_printer.py")

    #cmdline("sudo cp /var/www/html/gen_code/rw.py /var/www/html/d_imprimante"+str(p_number))
    #cmdline("sudo sed -i 's/#PRINTER_NUMBER#/"+str(p_number)+"/g' sed_remp.txt")
    
    cmdline("sudo mkdir /var/www/html/d_imprimante"+str(p_number)+"/uploads/")
    cmdline("sudo chmod 777 /var/www/html/d_imprimante"+str(p_number)+"/uploads/")
    #cmdline("sudo mv imprimante.php imprimante"+str(p_number)+".php")
    status = open(folder_name+"/status.txt","w")
    status.write("Free for printing")
    status.close()
    
    print("Folder n°"+str(p_number)+" created")


def force_reset():
    folder_nb = int(cmdline("ls | grep d_imprimante | wc -l"))
    for i in range (folder_nb):
        print("sudo rm -dr d_imprimante"+str(i))
        cmdline("sudo rm -dr d_imprimante"+str(i))
    printers_folders_update()
    
    
def index_update():
    index = open("index.php","r+")
    new_index = open("new_index.php","a+")
    
    index_lines = [line.strip() for line in index]
    
    b_new_index_lines = index_lines[:73]
    e_new_index_lines = index_lines[-24:]
    
    for i in b_new_index_lines:
        new_index.write(i)
        new_index.write("\n")

    
    folders = cmdline("ls | grep d_imprimante")
    folders_list = []
    folders_list = [str(j) for j in folders.split(b'\n')]
    del folders_list[-1]
    
    for i in folders_list:
        new_index.write("<option value=\""+str(i[14:-1])+"\">Printer "+str(i[14:-1])+ "</option>\n")
        
    new_index.write("<?php\n$option = $_POST['printer_nb'];\n$redirections = array(\n")
        
    for i in folders_list:
        new_index.write("'"+str(i[14:-1])+"' => 'd_imprimante"+str(i[14:-1])+"/imprimante.php',\n")
    
    
    for i in e_new_index_lines:
        new_index.write(i)
        new_index.write("\n")
        
        
    new_index.close()
    index.close()
    
    cmdline("sudo rm /var/www/html/index.php")
    cmdline("sudo mv /var/www/html/new_index.php /var/www/html/index.php")

force_reset()
index_update()