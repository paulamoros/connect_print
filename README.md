# Management of a 3D printer fleet

A project for the Fabricarium of Polytech Lille

## Context

This projet was suggested by the Fabricarium of Polytech Lille to embedded systems students as a 3rd and 4th year projet.
This lead to the first version of Connectprint. As this first version was not completely functional, the project has been continued to make a base tool for the Fabricarium that could work correctly with at least basic functionnalities.
This is the new version, worked from may to june 2023, with basic control and monitoring tools, but also some issues that must be fixed.
All the code has been written and tested on a Raspberry, that hosts the website to remotely control the 3D printers, connected to the RPi with USB serial link.
On the Raspberry, all the control, data gathering, and overall management of the system is written is Python, the website uses PHP code, with some Javascript parts
The printers used to develop this projet are Dagomas printers. Some issues could happen if other printer models are used, as no tests have been made on other models.

## Usage and features

When you download the git deposit, 
First, execute the make command to generate all the file tree and the structure of the website.
The make command executes the setup.py script. It must be executed with super user rights as all of the structuration commands are executed in the /var/etc/html (where the website is setup) folder.
When changes are made in some scripts, or when the number of printer linked to the Raspberry changes, the make clean command cleans all the printer folders and other files generated when using the system, so they can be regenerated properly with make.

Some libraries and features must be installed on the Raspberry to have the system working as:
  - 
  
  
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

The grep is used to get only the printers linked. The printer used in the Fabricarium are detected as following with this command:
```bash
Bus 001 Device 005: ID 0403:6001 Future Technology Devices International, Ltd FT232 Serial (UART) IC
```

If other printer models are used, some changes in the code should be made to make sure that the system detect the other printers, whose name is is different.
The ttyUSB and the name are linked with a folder, generated with all the codes used to manage the printer in a folder named "d_imprimanteX".
These 3 informations that describes a printer are saved in the printer_infos.txt file, in a list that contains this trio of elements for each printer.

Once the make is executed with no errors, everything is in place to use the system.

The website is reachable with the ip adress of the RPi, depending on its network.

The index.php page allows the user to choose one of the printer, then he can upload a g-code file, and the launch an impression on the printer.


## Website

The website installed on the Raspberry
The fronted part is mainly constituted by the webpages part.


## System

The 'gen_code' folder contains all the generic codes copied in the printer folders, with some modifications when the codes needs to "know" in wich folder they are.






## Common issues

status not updated



## Next steps

security
archives management

