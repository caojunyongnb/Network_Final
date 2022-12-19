from load_model import load_model
import networkx as nx
from Huangsice import generate_graph
class graph_compare():
    def __init__(self, filename, theta, T):
        self.filename=filename
        self.theta=theta
        self.T=T
    def generate_original_graph(self):
        #  will return original_graph and random graph
        ft = load_model(self.filename, theta=self.theta, T=self.T)
        graph = ft.graphMitload()
        ERgrpah, BAgraph = ft.generate_ERBA()
        return graph,ERgrpah,BAgraph
    # ruturn broken graph under 4 attack
    def attack_three_graph(self):
        graph,ERgrpah, BAgraph=self.generate_original_graph()
        md=generate_graph(self.filename, self.theta, T=self.T)
        # md.generate_original()
        md.input_outter_graph(graph)
        usPowerGrid_original,usPowerGrid_node,usPowerGrid_spc,usPowerGrid_ll,usPowerGrid_hl = md.get_all()
        md.input_outter_graph(ERgrpah)
        ERgrpah_original, ERgrpah_node, ERgrpah_spc, ERgrpah_ll, ERgrpah_hl = md.get_all()
        md.input_outter_graph(BAgraph)
        BAgraph_original, BAgraph_node, BAgraph_spc, BAgraph_ll, BAgraph_hl = md.get_all()
        return{'us':[usPowerGrid_original,usPowerGrid_node,usPowerGrid_spc,usPowerGrid_ll,usPowerGrid_hl],
               'er':[ERgrpah_original, ERgrpah_node, ERgrpah_spc, ERgrpah_ll, ERgrpah_hl],
               'ba':[ BAgraph_original, BAgraph_node, BAgraph_spc, BAgraph_ll, BAgraph_hl]}
if __name__=='__main__':
    gc=graph_compare('power-US-Grid.mtx', theta=0.1, T=1.3)
    result=gc.attack_three_graph()
    print('--------------------------------')
    print(len(result['us'][0].edges()))
    print(len(result['us'][1].edges()))
    print(len(result['us'][2].edges()))
    print(len(result['us'][3].edges()))
    print(len(result['us'][4].edges()))
    print('--------------------------------')

    print(len(result['er'][0].edges()))
    print(len(result['er'][1].edges()))
    print(len(result['er'][2].edges()))
    print(len(result['er'][3].edges()))
    print(len(result['er'][4].edges()))
    print('--------------------------------')

    print(len(result['ba'][0].edges()))
    print(len(result['ba'][1].edges()))
    print(len(result['ba'][2].edges()))
    print(len(result['ba'][3].edges()))
    print(len(result['ba'][4].edges()))

# 对比三种模型的结构
# 进行attack
