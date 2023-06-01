import os
import sys
import plotly.graph_objects as go
import time
import serial
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
    

def graph_ini(folder_name):
    
    fig=go.Figure()
    fig.update_layout(
        title='Temperature evolution',
        xaxis=dict(
            
            
            fixedrange=True,
            rangeslider=dict(visible=False)
        ),
        yaxis=dict(fixedrange=True)
    )
    
    file_path = os.path.join(folder_name, "graph.html")
    
    fig.write_html(file_path)
    print("Graph initialized")


if len(sys.argv[1]):
    graph_ini(sys.argv[1])
    print("graph inistialized \n\n\n")
    cmdline("python "+sys.argv[1]+"/data*.py > /dev/null 2>&1 &")
    
    
else:
    print("Please retry with only one argument")