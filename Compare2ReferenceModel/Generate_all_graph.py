import networkx as nx
from load_model import load_model
from iterate_simulation_for_edge import attack_simulation_algorithm
from iterate_simulation_for_node import attack_simulation_algorithm_node
# 调整T就是调整不同的capacity
class generate_graph():
    def __init__(self,filename,theta,T):
        self.T=T
        self.filename=filename
        self.theta=theta
    def generate_original(self):
        lm = load_model(self.filename, theta=self.theta, T=self.T)
        original = lm.graphMitload()
        self.original=original
    def input_outter_graph(self,graph):
        self.original=graph

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
        original=self.original

        node_attack_model = attack_simulation_algorithm_node(original)
        db_centrality = self.calculate_centrality(original, 'DB')
        #这是node attack返回的图
        nodebroken_graph=self.autorun_node(node_attack_model, db_centrality)


        original = self.original
        spc_criterion = attack_simulation_algorithm(original)
        original = self.original
        ll_criterion = attack_simulation_algorithm(original)
        original = self.original
        hl_criterion = attack_simulation_algorithm(original)

        spc_graph=self.autorun_edge(spc_criterion,"SPC")
        ll_grpah=self.autorun_edge(ll_criterion, "LL")
        hl_graph=self.autorun_edge(hl_criterion, "HL")

        return original,nodebroken_graph,spc_graph,ll_grpah,hl_graph

if __name__=='__main__':
    #调整T就是调整不同的capacity
    # theata就是初始的负载
    md=generate_graph('power-US-Grid.mtx', theta=1.2, T=10)
    #a,b,c,d,e
    # a 是原始图
    # b 是根据node破坏的图
    # c是spc策略破坏的图
    # d是ll策略破坏图
    # e是hl策略破坏图
    md.generate_original()

    a,b,c,d,e=md.get_all()
    # original = load_model()
    print(len(a.edges()))
    print(len(b.edges()))
    print(len(c.edges()))
    print(len(d.edges()))
    print(len(e.edges()))