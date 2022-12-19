from with_null_model import graph_compare
import numpy as np


gc = graph_compare('power-US-Grid.mtx', theta=0.1, T=1.3)
result = gc.attack_three_graph()
# [0.1,0.5,0.9,1.1,1.2,1.3,1.4,1.7,1.9,2.1,2.2,2.3,2.35,2.5]
for theta in [0.5,1.2,1.7]:
    us_list=[]
    er_list=[]
    ba_list=[]
    for T in np.arange(1.0,2,0.02):
        gc = graph_compare('power-US-Grid.mtx', theta=theta, T=T)
        result = gc.attack_three_graph()

        us_original_edges=len(result['us'][0].edges())
        us_node_edges=len(result['us'][1].edges())
        us_spc_edges=len(result['us'][2].edges())
        us_ll_edges=len(result['us'][3].edges())
        us_hl_edges=len(result['us'][4].edges())
        us_list.append([theta, T, us_node_edges/us_original_edges,us_spc_edges/us_original_edges,
                        us_ll_edges/us_original_edges,us_hl_edges/us_original_edges])

        er_original_edges=len(result['er'][0].edges())
        er_node_edges=len(result['er'][1].edges())
        er_spc_edges=len(result['er'][2].edges())
        er_ll_edges=len(result['er'][3].edges())
        er_hl_edges=len(result['er'][4].edges())
        er_list.append([theta, T, er_node_edges/er_original_edges,er_spc_edges/er_original_edges,
                        er_ll_edges/er_original_edges,er_hl_edges/er_original_edges])

        ba_original_edges=len(result['ba'][0].edges())
        ba_node_edges=len(result['ba'][1].edges())
        ba_spc_edges=len(result['ba'][2].edges())
        ba_ll_edges=len(result['ba'][3].edges())
        ba_hl_edges=len(result['ba'][4].edges())
        ba_list.append([theta, T, ba_node_edges/ba_original_edges,ba_spc_edges/ba_original_edges,
                        ba_ll_edges/ba_original_edges,ba_hl_edges/ba_original_edges])



    np.savetxt("Result/US"+str(theta)+".csv",
               us_list,
               delimiter=",",
               fmt='% s')

    np.savetxt("Result/ER"+str(theta)+".csv",
               er_list,
               delimiter=",",
               fmt='% s')

    np.savetxt("Result/BA"+str(theta)+".csv",
               ba_list,
               delimiter=",",
               fmt='% s')

