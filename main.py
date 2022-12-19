# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv

import load_model
from load_model import load_model
from iterate_simulation import *
# 这个就是创建了那个loadmodel的对象然后返回的load_graph就是我们需要的负载模型，
from iterate_simulation_for_node import attack_simulation_algorithm_node
"""lm = load_model('power-US-Grid.mtx', theta=1.2, T=1.2)
load_graph = lm.graphMitload()"""



def autorun(model,name):
        #model.initial_break_strategy(name)
    graph = model.initial_break(name)
    graph,broken_edge_dict = model.break_the_edge(graph)
    model.refresh_load(graph, broken_edge_dict)
    model.iterate_algorithm()

    return model.getRemainEdge()


"""spc_criterion = attack_simulation_algorithm(load_graph)
ll_criterion = attack_simulation_algorithm(load_graph)
hl_criterion = attack_simulation_algorithm(load_graph)

autorun(spc_criterion,"SPC")
autorun(ll_criterion, "LL")
autorun(hl_criterion, "HL")"""

def grid_search_run():
    res = []
    for theta in [0.1,0.5,0.9,1.1,1.2,1.3,1.4,1.7,1.9,2.1,2.2,2.3,2.35,2.5]:
        for t in np.arange(1.0,2.0,0.02):
            lm = load_model('power-US-Grid.mtx', theta=theta, T=t)
            load_graph = lm.graphMitload()

            spc_criterion = attack_simulation_algorithm(load_graph)
            ll_criterion = attack_simulation_algorithm(load_graph)
            hl_criterion = attack_simulation_algorithm(load_graph)

            spc = autorun(spc_criterion, "SPC")
            ll = autorun(ll_criterion, "LL")
            hl = autorun(hl_criterion, "HL")

            res.append([theta,t,spc,ll,hl])

            print("theta = "+str(theta)+ " , t = " + str(t) + " is completed!")


    return res

def grid_search_run_node():
    res = []
    for theta in [0.1,0.5,0.9,1.1,1.2,1.3,1.4,1.7,1.9,2.1,2.2,2.3,2.35,2.5]:
        for t in np.arange(1.0,2.0,0.02):
            lm = load_model('power-US-Grid.mtx', theta=theta, T=t)
            load_graph = lm.graphMitload()

            criterion = attack_simulation_algorithm_node(load_graph)

            db_centrality = criterion.calculate_centrality(load_graph, 'DB')

            # DB
            db = criterion.node_autorun(criterion, db_centrality)
            # BB
            #bb = criterion.node_autorun(criterion, bb_centrality)


            res.append([db])

            print("theta = "+str(theta)+ " , t = " + str(t) + "is completed!")

    return res

fields = ['theta', 't', 'spc_result', 'll_result',"hl_result"]
res = grid_search_run()

np.savetxt("edge_simulation.csv",
           res,
           delimiter=",",
           fmt='% s')

res2 = grid_search_run_node()
np.savetxt("node_simulation.csv",
           res2,
           delimiter=",",
           fmt='% s')

