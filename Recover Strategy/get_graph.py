import networkx as nx
from load_model import load_model
from iterate_simulation_for_edge_huang import attack_simulation_algorithm
from iterate_simulation_for_node_huang import attack_simulation_algorithm_node

class generate_graph():
    def __init__(self,filename,theta,T):
        self.T=T
        self.filename=filename
        self.theta=theta
    def generate_original(self):
        lm = load_model(self.filename, theta=self.theta, T=self.T)
        original = lm.graphMitload()
        return original

    def autorun_edge(self,model,name):
        #model.initial_break_strategy(name)
        graph = model.initial_break(name)
        graph,broken_edge_dict = model.break_the_edge(graph)
        model.refresh_load(graph, broken_edge_dict)
        final_graph=model.iterate_algorithm()
        return final_graph
    def autorun_node(self,model,centrality):
        #model.initial_break_strategy(name)
        graph = model.initial_break(centrality)
        graph,broken_edge_dict = model.break_the_edge(graph)
        model.refresh_load(graph, broken_edge_dict)
        final_graph=model.iterate_algorithm()
        return final_graph
    def calculate_centrality(self,load_model,strategy):
        if strategy=='BB':
            centrality=nx.betweenness_centrality(load_model,weight='initial_load')
        elif strategy=='DB':
            centrality = nx.degree_centrality((load_model))
        return centrality
    def get_all(self):
        original=self.generate_original()

        node_attack_model = attack_simulation_algorithm_node(original)
        db_centrality = self.calculate_centrality(original, 'DB')
        
        nodebroken_graph=self.autorun_node(node_attack_model, db_centrality)


        original = self.generate_original()
        spc_criterion = attack_simulation_algorithm(original)
        original = self.generate_original()
        ll_criterion = attack_simulation_algorithm(original)
        original = self.generate_original()
        hl_criterion = attack_simulation_algorithm(original)

        spc_graph=self.autorun_edge(spc_criterion,"SPC")
        ll_grpah=self.autorun_edge(ll_criterion, "LL")
        hl_graph=self.autorun_edge(hl_criterion, "HL")

        return original,nodebroken_graph,spc_graph,ll_grpah,hl_graph




md=generate_graph('power-US-Grid.mtx', theta=1.2, T=10)
#a,b,c,d,e
# a is original graph
# b is broken graph
# c is based on spc
# d is based on ll
# e is based on hl
a,b,c,d,e=md.get_all()
# original = load_model()
print(len(a.edges()))
print(len(b.edges()))
print(len(c.edges()))
print(len(d.edges()))
print(len(e.edges()))
