import plotly.graph_objects as go
import pandas as pd

print("beggining")
# Lire les données de température à partir du fichier texte
def read_temperature_data(file_path):
    temp_file = open("temp.txt","r")
    lines = temp_file.readlines()
    temp_file.close()
    data = []
    
    for i in range(0,len(lines)):
        line = eval(lines[i])
        data.append(line)
        
    df = pd.DataFrame(data, columns=['Temperature', 'Timestamp'])
    return df


# Create graph with Plotly
def update_graph():
    df = read_temperature_data('temp.txt')
    print(df)
    
    fig = go.Figure(data=go.Scatter(x=df['Timestamp'], y=df['Temperature']))
    fig.update_layout(
        title='Évolution de la température',
        xaxis_title='Temps',
        yaxis_title='Température (°C)',
        template='plotly_white'
    )
    fig.show()
    graph_html = fig.to_html(full_html=False)
    
    with open('graph.html', 'w') as file:
        file.write(graph_html)
    
    

# Appeler la fonction pour créer le graphe
create_temperature_graph()

while True:
    update_graph()
    time.sleep(10)