import copy

import networkx as nx
import numpy as np


class attack_simulation_algorithm():
    def __init__(self,load_model):
        self.load_model = load_model # original load model, unchanged through whole process
        self.last_broken_edge_dict = {} #save the last modified edges, together with current_load of these edges
        self.last_graph = copy.deepcopy(load_model) # create a deepcopy of the original model, this will be modified

        self.iteration = 0 # record how many iterations there are
        self.history_iteration_value = [] # history iteration values

    def initial_break_strategy(self,strategy_name):
        return self.Strategy(strategy_name)


    # implementation of three different attack strategies
    # SPC: largest proportion of the capacity of the attacked edge and the total capacities of the neighboring edges
    # HL (LL): the highest(lowest) initial_load of the graph
    def Strategy(self,name):
        initial_load_list = nx.get_edge_attributes(self.load_model, 'initial_load')
        index = []
        if name == "SPC": # SPC strategy
            spc_value = []
            for edge in self.load_model.edges:
                connected_edges = self.load_model.edges(edge)
                sum = 0
                for node_pair in connected_edges:
                    sum += self.get_edge_property_value(initial_load_list,node_pair)
                edge_load = self.get_edge_property_value(initial_load_list,edge)
                spc_value.append(edge_load / (sum - edge_load))
            index = np.argpartition(np.array(spc_value),-10)[-10:]
        elif name == "LL":
            index = np.argpartition(np.array(list(initial_load_list.values())), 10)[0:10]  # ten lowest value
        elif name == "HL":
            index = np.argpartition(np.array(list(initial_load_list.values())),-10)[-10:] # ten highest value

        edge_list = np.array(self.load_model.edges)[index]

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
        for edge in edge_list.tolist():
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
    '''
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    iterate就是一步一步的进行传播了，就是先破坏再再分配，然后再破坏，另外还缺一个迭代过程判断边是否需要破坏的函数，上面那个只是初始状态破坏哪一些，
    还没写每一步迭代的时候需要破坏哪些
    另外还有一点想法，或许可以作为一点咱们的创新点你考虑一下
    # 目前存在的问题，当一开始的电网刚开始崩塌的时候，这种再分配确实会存在，但是当大规模崩塌发生的时候，很多发电站以及用户节点就会降低，这样的话负载值相应的应该也会降低
    # 上面这个或许可以通过再写一个refresh函数来解决，就是说第一个崩溃后的refresh完成后，第二个refresh根据某种比例降低current load的值

    '''
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
            return graph
        self.iterate_algorithm()
        return graph

    def getRemainEdge(self):
        return len(self.last_graph.edges)



if __name__=='__main__':

    from load_model import load_model
    # 这个就是创建了那个loadmodel的对象然后返回的load_graph就是我们需要的负载模型，
    lm = load_model('power-US-Grid.mtx', theta=1.2, T=1.2)
    load_graph = lm.graphMitload()
    nx.write_gml(load_graph,'original.gml',stringizer=str)



    def autorun(model,name):
        #model.initial_break_strategy(name)
        graph = model.initial_break(name)
        graph,broken_edge_dict = model.break_the_edge(graph)
        model.refresh_load(graph, broken_edge_dict)
        model.iterate_algorithm()
        return model



    spc_criterion = attack_simulation_algorithm(load_graph)
    ll_criterion = attack_simulation_algorithm(load_graph)
    hl_criterion = attack_simulation_algorithm(load_graph)

    #autorun(spc_criterion,"SPC")
    #autorun(ll_criterion, "LL")
    autorun(hl_criterion, "HL")


