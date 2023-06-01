# Management of a 3D printer fleet

A project for the Fabricarium of Polytech Lille

## Context

This projet was suggested by the Fabricarium of Polytech Lille to embedded systems speciality students as a 3rd and 4th year projet.
This lead to the first version of Connectprint. As this first version was not completely functional, the project has been continued to make a base tool for the Fabricarium that could work correctly with at least basic functionnalities.
This is the new version, worked from may to june 2023, with basic control and monitoring tools, but also some issues that must be fixed.
All the code has been written and tested on a Raspberry, that hosts the website to remotely control the 3D printers, connected to the RPi with USB serial link.
On the Raspberry, all the control, data gathering, and overall management of the system is written is Python, the website uses PHP code, with some Javascript parts
The printers used to develop this projet are Dagomas printers. Some issues could happen if other printer models are used, as no tests have been made on other models.

## Usage

The git deposit must be cloned in the website folder, usually /var/www/html on a Raspberry.
Execute the make command to generate all the file tree and the structure of the website.
The make command executes the setup.py script. It must be executed with super user rights as all of the structuration commands are executed in the /var/etc/html (where the website is setup) folder.
When changes are made in some scripts, or when the number of printer linked to the Raspberry changes, the make clean command cleans all the printer folders and other files generated when using the system, so they can be regenerated properly with make.

Some libraries and packages must be installed on the Raspberry to have the system working as:
  - lighttpd as a webserver (you must also configure it)
  - pandas and plotly to manage the temperature datas and render it
  - php and javascript to execute the server-parts of the webpages codes
  - other packages may be required, check the error messages to see which ones, I may have forgotten some
  
The python scripts use the subprocess library, to create the following function:

```python
from subprocess import PIPE, Popen

def cmdline(command):
        process = Popen(
                args=command,
                stdout=PIPE,
                shell=True
        )
        return process.communicate()[0]
```

This function allows to execute bash commands on the Rasberry like python code using a pipe, and the output is caught by the script.

When executing the setup.py (or make) script, all the 3D printers are detected, with the /dev/ttyUSBX that are generated when a USB device is linked to the Rasberry via a serial link.
The first thing is to link a ttyUSB to a printer name, that we can get with:

```bash
lsusb | grep Future
```

The grep is used to get only the printers linked. The printer used in the Fabricarium are detected as follows with this command:
```bash
Bus 001 Device 005: ID 0403:6001 Future Technology Devices International, Ltd FT232 Serial (UART) IC
```

If other printer models are used, some changes in the code should be made to make sure that the system detect the other printers, whose name is is different.
The ttyUSB and the device name are linked with a folder, generated with all the codes used to manage the printer in a folder named "d_imprimanteX".
These 3 informations that describes a printer are saved in the printer_infos.txt file, in a list that contains this trio of elements for each printer.

Once the make is executed with no errors, everything is in place to use the system.

The website is reachable with the ip adress of the RPi, depending on its network.

The index.php page allows the user to choose one of the printer, then he can upload a g-code file, and the launch an impression on the printer.


## Website

This frontend part is composed of the php file tree. On the root of the server (/var/www/html), there is the index.php, modified when a new setup.py/make is executed, to create the right number of printers in the drop-down selection menu.
When a printer is selected, the user is redirected in the d_imprimanteX folder, to the imprimante.php page where he can upload his g-code file.
Some security is setup to make sure that the file is not too heavy and that it is a g-code file (.g).
If the file passes the tests, it is uploaded on the website in d_imprimanteX/uploads/, and the redirection button to the printer interface appears.

The interface.php page is also in every d_imprimante/ folder.
On the page loading, the informations about the 3D model to be printed are extracted from the g-code by piece_information.py and displayed on the website.

All the python scripts executed are executed with the shell_exec(command) php command from the website. On the Raspberry, it is the user "www-data" that executes the scripts, and this user doesn't own super user rights.
The codes must be written taking into account that the website can't execute su commands. This is why some text files and python script are vulnerable regarding the security of the system because openned in reading, writing and execution to all users.
A closer look on the system security should be made as it is not a part currently developped on the project.

If the printer is free and cleaned, the user can start an impression. The print.py and timer.py scripts (in d_imprimanteX/) are excuted in backgroud, so the webpage does not wait the end of the scripts to execute others.

```php
shell_exec('script.py > /dev/null 2>&1 &');
```

The print.py script takes in charge the update of the printer status, written in status.txt. The different status modes are:
  - Free for printing
  - Printing
  - Stopped
  - Print finished

The script can be executed only when the printer is free for printing. When print.py is executed, the status changes into "Printing". When the printing is finished, the status changes to "Print finished".
There are some other functionalities to control the printer available. The print process can be killed, clicking the "Stop printing" button, or simply paused or resumed with the 

## System

The 'gen_code' folder contains all the generic codes copied in the printer folders, with some modifications when the codes needs to "know" in wich folder they are.


The signal library is used to manage inter-process communication (IPC), so the print.py script can receive from control_printer.py the informations to stop, pause, or resume the printing.
As the website user on the RPi is a normal user, it can only use the SIGUSR1 and SIGUSR2 for the IPC. Other signals can only be used by super users.


## Common issues

Some issues have been detected while making tests of the system.

On the printer interface, it may occur that the status displayed is on "Printing" at the page loading, but the status.txt file contains "Free for printing".
No reason for this issue has been found yet.

The signals handling between control_printer.py and print.py can also have issues. The buttons of stop / resume on the interface may not always work properly.


## Next steps

security
archives management

