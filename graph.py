import networkx as nx
import matplotlib.pyplot as plt
import random

# Create a fully connected graph with 100 nodes
G = nx.complete_graph(50)

# Assign random weights to each edge
for (u, v) in G.edges():
    G[u][v]['weight'] = random.uniform(10, 20)

# Draw the graph
plt.figure(figsize=(20, 20))
pos = nx.spring_layout(G, seed=42)  # Position nodes using Fruchterman-Reingold force-directed algorithm
nx.draw(G, pos, node_size=50, with_labels=False, edge_color='gray', alpha=0.9)
nx.draw_networkx_edges(G, pos, alpha=0.3)

# Show the plot
plt.savefig("graph.png")
plt.show()
