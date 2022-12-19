# this would  feed into undirected unweighted adjcent matrix and generate the networkx graph
class load_model():
    def __init__(self,filename,theta=1.2,T=1.2):
        self.Path='Data/'+filename
        self.theta=theta
        self.T=T

    def data_loader(self):
        import scanpy as sc
        adata=sc.read(self.Path)
        return adata.X

    def data2graph(self):
        # generate basic graph from mtx
        import networkx as nx
        graph_data=self.data_loader()
        graph=nx.from_scipy_sparse_matrix(graph_data)
        return graph

    def graphMitload(self):
        import networkx as nx
        #generate load and capacety
        theta=self.theta
        T=self.T
        graph=self.data2graph()
        print(type(graph.degree()))
        for edge in graph.edges:
            node1=edge[0]
            node2=edge[1]
            degree1=graph.degree(node1)
            degree2 = graph.degree(node2)
            load=pow((degree1+1)*(degree2+1),theta)
            capacity=T*load
            nx.set_edge_attributes(graph,{edge:{'initial_load':load,'capacity':capacity,'current_load':load}})
        return graph

    def AddgraphMitload(self,rgraph):
        import networkx as nx
        #generate load and capacety
        theta=self.theta
        T=self.T
        graph=rgraph
        print(type(graph.degree()))
        for edge in graph.edges:
            node1=edge[0]
            node2=edge[1]
            degree1=graph.degree(node1)
            degree2 = graph.degree(node2)
            load=pow((degree1+1)*(degree2+1),theta)
            capacity=T*load
            nx.set_edge_attributes(graph,{edge:{'initial_load':load,'capacity':capacity,'current_load':load}})
        return graph
    def generate_ERBA(self):
        import networkx as nx
        # ER_graph = nx.erdos_renyi_graph(4941, 0.000528)
        ER_graph = nx.erdos_renyi_graph(4941, 0.001)
        BA_graph = nx.barabasi_albert_graph(4941, 2, seed=None)
        ER_graph_load=self.AddgraphMitload(ER_graph)
        BA_graph_load = self.AddgraphMitload(BA_graph)
        return ER_graph_load,BA_graph_load



    # def generate_
if __name__=='__main__':
    import networkx as nx
    ft = load_model('power-US-Grid.mtx', theta=1.2, T=1.2)
    graph = ft.graphMitload()
    ERgrpah,BAgraph=ft.generate_ERBA()

    print(len(graph.edges()))
    print(len(ERgrpah.edges()))
    print(len(BAgraph.edges()))

