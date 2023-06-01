import os
import sys
import plotly.graph_objects as go


def graph_ini(folder_name):
    
    fig=go.Figure()

    file_path = os.path.join(folder_name, "graph.html")
    
    fig.write_html(file_path)
    print("Graph initialized")


if len(sys.argv[1]):
    graph_ini(sys.argv[1])
    
else:
    print("Please retry with only one argument")