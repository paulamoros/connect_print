import plotly.graph_objects as go
import pandas as pd
import time
import os
import fcntl
 
lock_file = os.path.abspath(__file__)

try:
    file_handle = open(lock_file, "w")
    fcntl.flock(file_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)

except IOError:
    print("The data script is already running.")
    sys.exit(0)
    
# Read temperature data from text file
def read_temperature_data():
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_path = script_dir+"/temp.txt"
    
    temp_file = open("temp.txt","w")
    temp_file.close()        
    temp_file = open("temp.txt","r")
        
    lines = temp_file.readlines()
    temp_file.close()
    data = []
        
    if (len(lines) > 0):
        for i in range(0,len(lines)):
            line = eval(lines[i])
            data.append(line)
        
    else:
        print("temp.txt empty")
        
    df = pd.DataFrame(data, columns=['Temperature', 'Timestamp'])
        
    return df
        

# Create graph with Plotly
def update_graph():
    df = read_temperature_data()
    print(df)
    
    fig = go.Figure(data=go.Scatter(x=df['Timestamp'], y=df['Temperature']))
    fig.update_layout(
        title='Temperature evolution',
        xaxis_title='Time',
        yaxis_title='Température (°C)',
        xaxis=dict(
            fixedrange=True,
            rangeslider=dict(visible=False)
        ),
        yaxis=dict(fixedrange=True)
        
        template='plotly_white'
    )
    fig.show()
    graph_html = fig.to_html(full_html=False)
    
    with open('graph.html', 'w') as file:
        file.write(graph_html)

try: 
    while True:
        update_graph()
        time.sleep(10)

# then whatever the error is, we need to free the lock
finally:
    fcntl.flock(file_handle, fcntl.LOCK_UN)
    file_handle.close()
