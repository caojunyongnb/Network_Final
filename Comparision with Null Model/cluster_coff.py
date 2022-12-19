from with_null_model import graph_compare
import networkx as nx
from scipy.stats import pearsonr
gc = graph_compare('power-US-Grid.mtx', theta=0.1, T=1.3)
result = gc.attack_three_graph()


print(nx.average_clustering(result['us'][0]))
print(nx.average_clustering(result['er'][0]))
print(nx.average_clustering(result['ba'][0]))

CC=nx.clustering(result['us'][0])

DC=nx.degree_centrality(result['ba'][0])
# 0.08010361108159711
# 0.0008317336489771218
# 0.006819003455210073
ccl=[]
dcl=[]
for i in DC.keys():
    ccl=ccl+[CC[i]]
    dcl = dcl + [DC[i]]
print(pearsonr(ccl,dcl))