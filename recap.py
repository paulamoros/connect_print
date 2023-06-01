#!/usr/bin/env python

#This script is used to format the status and temperature informations about the printers, using for each printer the files status.txt and temp.txt
def recap_update():
    recap_lines = ""
    
    folders = open("printers_infos.txt", "r")
    line = folders.readlines()
    folders_list = eval(line[0])
    
    for i in folders_list:
        folder_name = i[2][2:-1]
        folder_nb = folder_name[12:]
        
        status = open("/var/www/html/"+folder_name+"/status.txt", "r")
        str_status = status.readlines()[0]
        status.close()
        
        temp = open("/var/www/html/"+folder_name+"/temp.txt", "r")
        str_temps = temp.readlines()
        temp.close()
        
        if len(str_temps) == 0:
            str_temp = "No temperature recorded"
        else:
            str_temp = str(eval(str_temps[-1])[0])+"°C"
        
        recap_lines = recap_lines+"Printer n°"+folder_nb+":\nStatus: "+str_status+"\nLast recorded temperature: "+str_temp+"\n\n"
        
    recap = open("recap.txt", "w")
    recap.write("")
    
    recap = open("recap.txt", "a")
    recap.write(recap_lines)
    recap.close()
    
    return True
    
    
recap_update()