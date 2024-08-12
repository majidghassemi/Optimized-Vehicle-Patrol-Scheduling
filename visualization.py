import networkx as nx
import matplotlib.pyplot as plt

# Number of nodes
num_nodes = 50
# Edge probability
edge_prob = 0.099

# Generate a random graph
G = nx.erdos_renyi_graph(n=num_nodes, p=edge_prob)

# Draw the graph
plt.figure(figsize=(10, 10))
nx.draw(G, with_labels=True, node_color='lightblue', node_size=500, edge_color='gray')
plt.title("Random Network with 50 Nodes and Edge Probability 0.099")
plt.show()