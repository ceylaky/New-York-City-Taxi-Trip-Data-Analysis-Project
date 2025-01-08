import csv
import networkx as nx 
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict

def readfile(file_path: str) -> List[dict]:
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)      #making the data into a list of dictionaries
    return data

filepath = "/Users/ceylakaya/Desktop/small/nyc_dataset_small.txt"
data = readfile(filepath)

def buildgraph(data):
    G = nx.Graph()
    node_map = {}  # In this dictionary we are saving the mapping of pickup/dropoff location ID to node index
    
    # We iterate over the data to count trips between pickup and dropoff locations
    trip_counts = {}
    for entry in data:
        pickup = int(entry['PULocationID'])
        dropoff = int(entry['DOLocationID']) #we can use int because there are no float values in the data this time. 
        
        # This adds a pickup node in the case that there isn't already one.
        if pickup not in node_map:
            node_map[pickup] = len(G.nodes)
            G.add_node(len(G.nodes), location=pickup)
        
        # This adds a dropoff node in the case that there isn't already one.
        if dropoff not in node_map:
            node_map[dropoff] = len(G.nodes)
            G.add_node(len(G.nodes), location=dropoff)
        
        # Now we add edges between pickup and dropoff locations
        edge = (node_map[pickup], node_map[dropoff])
        trip_counts[edge] = trip_counts.get(edge, 0) + 1
    
    # And then we adjust the weight of the edges according to how many trips have been made. (EX: Thicker edge = more trips)
    for (pickup, dropoff), count in trip_counts.items():
        if G.has_edge(pickup, dropoff):
            G[pickup][dropoff]['weight'] += count    #we determine the weight here, we will use it while building the graph.
        else:
            G.add_edge(pickup, dropoff, weight=count)  
    
    return G



graph = buildgraph(data)

pos = nx.spring_layout(graph)  

# now we are using the weights we determined and here we add the edge weights to the graph.
edge_width = [data['weight'] / 10 for _, _, data in graph.edges(data=True)]

nx.draw_networkx_nodes(graph, pos, node_size=200)

nx.draw_networkx_edges(graph, pos, width=edge_width, alpha=0.5)

nx.draw_networkx_labels(graph, pos, font_size=12, font_family="sans-serif")

plt.axis('off')

plt.show()
