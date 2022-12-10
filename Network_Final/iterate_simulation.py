import networkx as nx


class attack_simulation_algorithm():
    def __init__(self,load_model):
        self.load_model=load_model
    '''
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    这个就是论文中有三种策略，每种策略都会在图中挑选一部分节点作为初始破坏点，需要做的就是，在load_model里面应用三种策略，选出不同的初始破坏点，
    然后输入的就是不同的strategy，输出的就是改strategy对应的edge_list
    '''
    def initial_break_stragy(self,strategy):
        #this should return a edge list by its strategy
        load_model=self.load_model
        count=0
        edge_list=[]
        for edge in load_model.edges():
            count=count+1
            if count==10:
                break
            edge_list=edge_list+[edge]

        self.edge_list=edge_list

    '''
    这就是我说的那个报错，如果直接获取边对应的property value的话会因为边那俩节点的顺序报错（那个函数假定的图是有向图，这里就是尝试不同的顺序
    然后来返回数据
    '''
    def get_edge_property_value(self,property_dict,value):
        # when try to get the edge property, the function refered the graph as directed graph, but we use underected graph
        # so sometimes the order will lead to the failure
        node1=value[0]
        node2 = value[1]
        result =0
        try:
            result=property_dict[node1,node2]
        except:
            result=property_dict[node2, node1]
        return result

    '''
    这个函数是对图进行初始化，给每条边加一个property ：if_break， 然后后面break的时候如果这个if_break为0就是不破坏，为1就是破坏
    另外这个函数就是上面不是选出来了需要三种策略下破坏的初始边，这里就把那些初始边标注为1
    '''
    def initial_break(self):
        import networkx as nx
        #feed into the nodelist and break the edges at the begin
        graph=self.load_model
        edge_list=self.edge_list
        nx.set_edge_attributes(graph,0, "if_break")
        for edge in edge_list:
            nx.set_edge_attributes(graph, {edge: {'if_break':1}})
        return graph

    '''
    这里就是把图里所有if_break为1的边给破坏掉，返回一个破坏之后的图，另外返回一个字典，字典的key是edge，value是该edge对应的current load
    '''
    def break_the_edge(self,graph):
        # remove the edge where the 'if_break' is 1, and return the graph and node has been removed and there current load
        edge_tb_remove=[]
        edge_be_removed={}
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
        return graph, edge_be_removed

    '''
    这一步就是输入破坏后的图以及上面那个字典，然后根据这个字典对周边的边进行新的current_load的更新
    或许会出现的问题，如果没出现就不要考虑了，如果一个edge的周边所有的edge都崩塌了，就孤立这一个edge然后如果他也崩塌咋办（就没法distribute了，
    目前代码没考虑，想了一下出现的概率应该不大，所以可以暂时不考虑
    '''
    def refresh_load(self,graph,broken_edge_dict):
        # this will input a graph, and broken_edge_dict, and return the redistributed graph
        #broken_edge_dict {edge:current_load}
        # we just consider the redistribution will only work on the edge directly connected edge, to simplify
        edge_current_load_list=nx.get_edge_attributes(graph, 'current_load')
        for broken_edge in broken_edge_dict.keys():
            #calculate the load need to be distributed
            node1 = broken_edge[0]
            node2 = broken_edge[1]
            degree1 = graph.degree(node1)
            degree2 = graph.degree(node2)
            distributed_load = broken_edge_dict[broken_edge] / (degree2 + degree1)
            # do the distribution
            edge_connected_to_node1=graph.edges(node1)
            edge_connected_to_node2 = graph.edges(node2)
            for edge_tob_distribute in list(edge_connected_to_node1)+list(edge_connected_to_node2):
                edge_current_load=self.get_edge_property_value(edge_current_load_list,edge_tob_distribute)
                # add distributed load to each edge
                nx.set_edge_attributes(graph, {edge_tob_distribute: {'current_load':edge_current_load+distributed_load}})
        return graph

    '''
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    就是我说的那个停止条件，在下面iterate的时候记得留一下这块的位置
    '''
    def stop_sign(self):
        return True
    '''
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    iterate就是一步一步的进行传播了，就是先破坏再再分配，然后再破坏，另外还缺一个迭代过程判断边是否需要破坏的函数，上面那个只是初始状态破坏哪一些，
    还没写每一步迭代的时候需要破坏哪些
    另外还有一点想法，或许可以作为一点咱们的创新点你考虑一下
    # 目前存在的问题，当一开始的电网刚开始崩塌的时候，这种再分配确实会存在，但是当大规模崩塌发生的时候，很多发电站以及用户节点就会降低，这样的话负载值相应的应该也会降低
    # 上面这个或许可以通过再写一个refresh函数来解决，就是说第一个崩溃后的refresh完成后，第二个refresh根据某种比例降低current load的值

    '''
    def iterate_algorithm(self):
        n=0
if __name__=='__main__':

    from load_model import load_model
    # 这个就是创建了那个loadmodel的对象然后返回的load_graph就是我们需要的负载模型，
    lm = load_model('power-US-Grid.mtx', theta=1.2, T=1.2)
    load_graph = lm.graphMitload()


    # asa就是创建一下上面那个对象，把生成的负载模型图给输入这个对象
    asa=attack_simulation_algorithm(load_graph)
    #这里就是选择你的streagy
    asa.initial_break_stragy('1')
    # 这个就是根据你的strategy标志一下哪些边需要断掉
    graph=asa.initial_break()
    #把上面的标注的边断掉
    graph,broken_edge_dict=asa.break_the_edge(graph)
    # 再分配一下
    after=asa.refresh_load(graph, broken_edge_dict)
    #这一部分最后整合一下，最理想就是选择完streagy之后，就直接start iterate就行
###

