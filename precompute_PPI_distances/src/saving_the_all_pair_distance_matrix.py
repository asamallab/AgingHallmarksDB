import pickle as pkl
import networkx as nx
import netmedpy


with open('../input/Human_PPI.pkl', 'rb') as file1:
    ppi = pkl.load(file1)
    
lcc_nodes = max(nx.connected_components(ppi), key=len)
ppi = ppi.subgraph(lcc_nodes).copy()

n_procs = 12

### Calculate shortest path distance matrix between node pairs
sp_distance = netmedpy.all_pair_distances(ppi, distance="shortest_path", 
                                          n_processors=n_procs, n_tasks=1000)

with open('../../proximity_computation/input/shortest_path_distances_Human_PPI.pkl', 'wb') as file:
    pkl.dump(sp_distance, file)
