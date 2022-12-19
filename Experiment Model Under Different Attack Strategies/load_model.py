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
            load=pow(degree1*degree2,theta)
            capacity=T*load
            nx.set_edge_attributes(graph,{edge:{'initial_load':load,'capacity':capacity,'current_load':load}})
        return graph



    # def generate_
if __name__=='__main__':
    import networkx as nx
    ft = load_model('power-US-Grid.mtx', theta=1.2, T=1.2)
    graph = ft.graphMitload()
    print(0)
