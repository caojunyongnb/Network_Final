import copy

import networkx as nx
import numpy as np


class attack_simulation_algorithm_node():
    def __init__(self,load_model):
        self.load_model = load_model # original load model, unchanged through whole process
        self.last_broken_edge_dict = {} #save the last modified edges, together with current_load of these edges
        self.last_graph = copy.deepcopy(load_model) # create a deepcopy of the original model, this will be modified
        self.iteration = 0 # record how many iterations there are
        self.history_iteration_value = [] # history iteration values


    #BB betweness_base
    #DB Degree_base
    def initial_break_strategy(self,strategy_name):
        return self.Strategy(strategy_name)

    def Strategy(self,centrality):
        import networkx as nx
        load_model=self.load_model
        node_top10_list = []
        ### betweeness centrality consider the weight of edge
        ### degree centrality dont consider, because the edge node are calculate base on the node degree
        centrality_sort={k: v for k, v in sorted(centrality.items(), key=lambda item: item[1])}
        counter=0
        for key in centrality_sort.keys():
            counter=counter+1
            node_top10_list=node_top10_list+[key]
            if counter== 3:
                break
        edge_list = []
        for node in node_top10_list:
            edge_list=edge_list+list(load_model.edges(node))
        return edge_list
    '''
    这就是我说的那个报错，如果直接获取边对应的property value的话会因为边那俩节点的顺序报错（那个函数假定的图是有向图，这里就是尝试不同的顺序
    然后来返回数据
    '''
    def get_edge_property_value(self,property_dict,value):
        # when try to get the edge property, the function refered the graph as directed graph, but we use underected graph
        # so sometimes the order will lead to the failure
        node1 = value[0]
        node2 = value[1]
        try:
            result = property_dict[node1,node2]
        except:
           result = property_dict[node2, node1]
        else:
            return result
        return result

    '''
    这个函数是对图进行初始化，给每条边加一个property ：if_break， 然后后面break的时候如果这个if_break为0就是不破坏，为1就是破坏
    另外这个函数就是上面不是选出来了需要三种策略下破坏的初始边，这里就把那些初始边标注为1
    '''
    def initial_break(self,name):
        import networkx as nx
        #feed into the nodelist and break the edges at the begin
        graph = self.last_graph
        edge_list = self.initial_break_strategy(name);
        nx.set_edge_attributes(graph,0, "if_break")
        for edge in list(edge_list):
            nx.set_edge_attributes(graph, {tuple(edge): {'if_break':1}})
        return graph

    '''
    这里就是把图里所有if_break为1的边给破坏掉，返回一个破坏之后的图，另外返回一个字典，字典的key是edge，value是该edge对应的current load
    '''
    def break_the_edge(self,graph):
        # remove the edge where the 'if_break' is 1, and return the graph and node has been removed and there current load
        edge_tb_remove=[]
        edge_be_removed ={}
        if_break_list=nx.get_edge_attributes(graph,'if_break')
        current_load_list = nx.get_edge_attributes(graph, 'current_load')
        # store the removed edge in the dict and remove them latter
        #get_edge_property_value(self,property_dict,value)
        for edge in graph.edges():
            if self.get_edge_property_value(if_break_list,edge)==1:
                edge_tb_remove=edge_tb_remove+[edge]
                graph.remove_edge(edge[0],edge[1])
                edge_be_removed[edge]=self.get_edge_property_value(current_load_list,edge)
        graph.remove_edges_from(edge_tb_remove)
        self.last_broken_edge_dict = edge_be_removed
        self.last_graph = graph
        return graph, edge_be_removed
    '''
    这一步就是输入破坏后的图以及上面那个字典，然后根据这个字典对周边的边进行新的current_load的更新
    或许会出现的问题，如果没出现就不要考虑了，如果一个edge的周边所有的edge都崩塌了，就孤立这一个edge然后如果他也崩塌咋办（就没法distribute了，
    目前代码没考虑，想了一下出现的概率应该不大，所以可以暂时不考虑
    '''
    def refresh_load(self,graph,broken_edge_dict):
        # this will input a graph, and broken_edge_dict, and return the redistributed graph
        # broken_edge_dict {edge:current_load}
        # we just consider the redistribution will only work on the edge directly connected edge, to simplify
        edge_current_load_list = nx.get_edge_attributes(graph, 'current_load')
        for broken_edge in broken_edge_dict.keys():
            """# calculate the load need to be distributed
            node1 = broken_edge[0]
            node2 = broken_edge[1]
            degree1 = graph.degree(node1)
            degree2 = graph.degree(node2)
            sum_degree = degree1 + degree2
            if sum_degree == 0:
                sum_degree = 1e-6
            distributed_load = broken_edge_dict[broken_edge] / sum_degree
            # do the distribution
            edge_connected_to_node1=graph.edges(node1)
            edge_connected_to_node2 = graph.edges(node2)"""
            broken_load = self.get_edge_property_value(self.last_broken_edge_dict,broken_edge)
            edges_tobe_distributed = list(self.last_graph.edges(broken_edge))
            sum = 0
            for edge in edges_tobe_distributed:
                edge_load = self.get_edge_property_value(edge_current_load_list,edge)
                sum += edge_load


            for edge_tob_distribute in edges_tobe_distributed:
                edge_current_load = self.get_edge_property_value(edge_current_load_list,edge_tob_distribute)
                # add distributed load to each edge
                nx.set_edge_attributes(graph, {edge_tob_distribute: {'current_load':edge_current_load + (broken_load*(edge_current_load / sum))}})

        self.last_graph = graph
        return graph

    '''
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    就是我说的那个停止条件，在下面iterate的时候记得留一下这块的位置
    '''

    def stop_sign(self,break_dict):
        #print(len(self.last_graph.edges))
        if len(self.history_iteration_value)<=10:
            self.history_iteration_value.append(len(self.last_graph.edges))
            return False
        if np.mean(self.history_iteration_value[-3:]) == len(self.last_graph.edges):
            self.history_iteration_value.append(len(self.last_graph.edges))
            return True
        self.history_iteration_value.append(len(self.last_graph.edges))
        return False

    def iterate_algorithm(self):
        #recursive algorithm, will repeatedly call itself if stop_sign condition isn't met
        tobe_break = {} # edges to be broken in this round, stored in dictionary format
        last_broken_edge_dict = self.last_broken_edge_dict
        graph = self.last_graph
        current_load_list = nx.get_edge_attributes(graph, 'current_load')
        capacity_load_list = nx.get_edge_attributes(graph, "capacity")
        for broken_edge in last_broken_edge_dict.keys():
            connected_edges = graph.edges(broken_edge) # all the connected edges to the two nodes
            for edge in connected_edges:
                #print(edge)
                current_load = self.get_edge_property_value(current_load_list,edge)
                capacity  = self.get_edge_property_value(capacity_load_list,edge)
                if(current_load > capacity):
                   tobe_break[edge] = self.get_edge_property_value(current_load_list, edge)
        for edge in tobe_break.keys():
            nx.set_edge_attributes(graph, {edge: {'if_break': 1}})
        self.break_the_edge(graph)
        self.refresh_load(self.last_graph,self.last_broken_edge_dict)
        self.iteration += 1
        #print("Iteration" + str(self.iteration))
        if self.stop_sign(tobe_break):
            return
        self.iterate_algorithm()

    def getRemainEdge(self):
        return len(self.last_graph.edges)

    def calculate_centrality(self,load_model,strategy):
        if strategy=='BB':
            centrality=nx. betweenness_centrality(load_model,weight='initial_load')
        elif strategy=='DB':
            centrality = nx.degree_centrality((load_model))
        return centrality

    def node_autorun(self,model,centrality):
        #model.initial_break_strategy(name)
        graph = model.initial_break(centrality)
        graph,broken_edge_dict = model.break_the_edge(graph)
        model.refresh_load(graph, broken_edge_dict)
        model.iterate_algorithm()
        return self.getRemainEdge()


"""
if __name__=='__main__':

    from load_model import load_model
    # 这个就是创建了那个loadmodel的对象然后返回的load_graph就是我们需要的负载模型，
    import networkx as nx
    def calculate_centrality(load_model,strategy):
        if strategy=='BB':
            centrality=nx. betweenness_centrality(load_model,weight='initial_load')
        elif strategy=='DB':
            centrality = nx.degree_centrality((load_model))
        return centrality
    lm = load_model('power-US-Grid.mtx', theta=1.2, T=1.2)
    load_graph = lm.graphMitload()

    def node_autorun(model,centrality):
        #model.initial_break_strategy(name)
        graph = model.initial_break(centrality)
        graph,broken_edge_dict = model.break_the_edge(graph)
        model.refresh_load(graph, broken_edge_dict)
        model.iterate_algorithm()
        return

    criterion = attack_simulation_algorithm_node(load_graph)
    # DB就是degree centrality BB就是Between centrality，BB慢很多，我这边就改了一下选择策略返回edgeList那块，其他完全没变

    db_centrality=calculate_centrality(load_graph,'DB')
    bb_centrality = calculate_centrality(load_graph, 'BB')
"""



