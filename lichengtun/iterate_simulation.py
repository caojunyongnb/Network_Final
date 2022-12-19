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
        capacity = nx.get_edge_attributes(self.load_model, 'capacity')
        index = []
        if name == "SPC": # SPC strategy
            spc_value = []
            for edge in self.load_model.edges:
                connected_edges = self.load_model.edges(edge)
                sum = 0
                #print(connected_edges)
                for node_pair in connected_edges:
                    sum += self.get_edge_property_value(capacity,node_pair)
                edge_load = self.get_edge_property_value(capacity,edge)
                spc_value.append(edge_load / (sum - edge_load))
            index = np.argpartition(np.array(spc_value),-10)[-10:]
        elif name == "LL":
            index = np.argpartition(np.array(list(initial_load_list.values())), 10)[0:10]  # ten lowest value
        elif name == "HL":
            index = np.argpartition(np.array(list(initial_load_list.values())),-10)[-10:] # ten highest value

        edge_list = np.array(self.load_model.edges)[index]

        return edge_list

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

    def initial_break(self,name):
        import networkx as nx
        #feed into the nodelist and break the edges at the begin
        graph = self.last_graph
        edge_list = self.initial_break_strategy(name);
        nx.set_edge_attributes(graph,0, "if_break")
        for edge in edge_list.tolist():
            nx.set_edge_attributes(graph, {tuple(edge): {'if_break':1}})

        return graph

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

    def stop_sign(self,break_dict):
        #print(len(self.last_graph.edges))
        if len(self.history_iteration_value)<=100:
            self.history_iteration_value.append(len(self.last_graph.edges))
            return False

        if np.mean(self.history_iteration_value[-20:]) == len(self.last_graph.edges):
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

        if self.stop_sign(tobe_break):
            return
        self.iterate_algorithm()

    def getRemainEdge(self):
        return len(self.last_graph.edges)

