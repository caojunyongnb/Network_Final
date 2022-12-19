import networkx as nx
import matplotlib.pyplot

or_g = nx.read_gml("./original.gml")
b_g = nx.read_gml("./broken.gml")

def get_degree_start(G, g): 
    degree_dict = dict(G.degree()) 
    start_list_n_v_sorted = sorted(degree_dict.items(),key=lambda k_v:k_v[1],reverse=True) 
    degree_b_dict = dict(g.degree()) 
    start_list_b_n_v_sorted = sorted(degree_b_dict.items(),key=lambda k_v:k_v[1],reverse=True)
    degree_n_list=[]
    degree_v_list=[]
    degree_b_v_list=[]
    for name,value in start_list_n_v_sorted:
        for n, v in start_list_b_n_v_sorted:
             if n == name and v != value:
                degree_n_list.append(name)
                degree_v_list.append(value)
                degree_b_v_list.append(v)
    
    diff = [degree_v_list[i] - degree_b_v_list[i] for i in range(len(degree_v_list))]
    start_index = diff.index(max(diff))  
    
    start_name = degree_n_list[start_index]
    
    return start_name

def get_degree_centrality_sort_neighbors(G, g): 
    degree_c_dict = dict(nx.degree_centrality(G))  
    list_n_v_sorted = sorted(degree_c_dict.items(),key=lambda k_v:k_v[1],reverse=True)  
    
    break_dict = dict(nx.degree_centrality(g))
    break_list_n_v_sorted = sorted(break_dict.items(),key=lambda k_v:k_v[1],reverse=True)
    
    degree_c_name_list = []
    degree_c_value_list = []
    degree_c_break_name_list = []
    degree_c_break_value_list = []
        
    for name,value in list_n_v_sorted:
        for n, v in break_list_n_v_sorted:
             if n == name and v != value:
                degree_c_break_name_list.append(name)
                degree_c_value_list.append(value)
                degree_c_break_value_list.append(v)
#     print(degree_c_value_list)
#     print(degree_c_break_name_list)
#     print(degree_c_break_value_list)
    return degree_c_value_list, degree_c_break_name_list, degree_c_break_value_list

def get_closeness_centrality_sort_neighbors(G, g): 
    closeness_c_dict = dict(nx.closeness_centrality(G))  
    list_n_v_sorted = sorted(closeness_c_dict.items(),key=lambda k_v:k_v[1],reverse=True)  
    
    break_dict = dict(nx.closeness_centrality(g))
    break_list_n_v_sorted = sorted(break_dict.items(),key=lambda k_v:k_v[1],reverse=True)
    
    closeness_c_name_list = []
    closeness_c_value_list = []
    closeness_c_break_name_list = []
    closeness_c_break_value_list = []
    
    for name,value in list_n_v_sorted:

        for n, v in break_list_n_v_sorted:
             if n == name and v != value:
                closeness_c_break_name_list.append(name)
                closeness_c_value_list.append(value)
                closeness_c_break_value_list.append(v)
#     print(closeness_c_value_list)
#     print(closeness_c_break_name_list)
#     print(closeness_c_break_value_list)
    return closeness_c_value_list, closeness_c_break_name_list, closeness_c_break_value_list

def get_betweenness_centrality_sort_neighbors(G, g): 
    betweenness_c_dict = dict(nx.betweenness_centrality(G))  
    list_n_v_sorted = sorted(betweenness_c_dict.items(),key=lambda k_v:k_v[1],reverse=True)  
    
    break_dict = dict(nx.betweenness_centrality(g))
    break_list_n_v_sorted = sorted(break_dict.items(),key=lambda k_v:k_v[1],reverse=True)
    
    betweenness_c_name_list = []
    betweenness_c_value_list = []
    betweenness_c_break_name_list = []
    betweenness_c_break_value_list = []
    
    for name,value in list_n_v_sorted:

        for n, v in break_list_n_v_sorted:
             if n == name and v != value:
                betweenness_c_break_name_list.append(name)
                betweenness_c_value_list.append(value)
                betweenness_c_break_value_list.append(v)
#     print(betweenness_c_value_list)
#     print(betweenness_c_break_name_list)
#     print(betweenness_c_break_value_list)
    return betweenness_c_value_list, betweenness_c_value_list, betweenness_c_break_value_list
def recover_anaylse_degree(G, g, lis_n, lis_v, lis_b_v, start):
    import copy    
    re_graph = copy.deepcopy(G)
    or_aver = nx.average_clustering(g)
    
    N = nx.number_of_nodes(g)
    sumeff = 0
    sumeff_b = 0
    for u in g.nodes(): 
        path = nx.shortest_path_length(g, source=u)
        for v in path.keys():  
            if u != v:  
                sumeff += 1 / path[v]
    result = (1 / (N * (N - 1))) * sumeff 
    
    step = len(lis_n)
    time_list = []
    aver_clu = []
    ef = []
    count = 0
    re_graph.add_edge(start, lis_n[0])
#   print(re_graph)

    while count < step:
        b_aver = nx.average_clustering(re_graph) 
        for u in re_graph.nodes(): 
            path = nx.shortest_path_length(re_graph, source=u)
            for v in path.keys():  
                if u != v:  
                    sumeff_b += 1 / path[v]
        result_b = (1 / (N * (N - 1))) * sumeff_b   
        for i in range(step): #or use for i in degree_break_name_list 
            if lis_v[i] == lis_b_v[i]:
                del lis_n[i]
            else:
                re_graph.add_edge(lis_n[i], lis_n[i])
                aver_clu.append(b_aver / or_aver)
                time_list.append(count)
                n = nx.number_of_nodes(re_graph)
                ef.append(result_b/result)
                
        count += 1
    
#     print(aver_clu)
#     print(time_list)
    return aver_clu, ef, time_list

if __name__ == '__main__':
    star = get_degree_start(or_g, b_g)
    dcv, dcbn, dcbv = get_degree_centrality_sort_neighbors(or_g, b_g)
    recover_anaylse_degree(b_g, or_g, dcbn, dcv, dcbv, star)
    dc_ac, dc_ef, dc_time = recover_anaylse_degree(b_g, or_g, dcbn, dcv, dcbv, star)
    
    ccv, ccbn, ccbv = get_closeness_centrality_sort_neighbors(or_g, b_g)
    recover_anaylse_degree(b_g, or_g, ccbn, ccv, ccbv, star)
    cc_ac, cc_ef, cc_time = recover_anaylse_degree(b_g, or_g, ccbn, ccv, ccbv, star)
    
    bcv, bcbn, bcbv = get_betweenness_centrality_sort_neighbors(or_g, b_g)
    recover_anaylse_degree(b_g, or_g, bcbn, bcv, bcbv, star)
    bc_ac, bc_ef, bc_time = recover_anaylse_degree(b_g, or_g, bcbn, bcv, bcbv, star)
    
    f = plt.figure(figsize=(60, 60))

    plt.tight_layout()
    pos = f.add_subplot(3,2,1) 
    plt.scatter(dc_time, dc_ef, s=70, c='deeppink', marker='o')
    plt.xlabel("Time")
    plt.ylabel("Ratio of original to restored network")
    plt.title('Efficiency base on degree centrality') 

    pos = f.add_subplot(3,2,2) 
    plt.scatter(dc_time, dc_ac, s=70, c='deeppink', marker='o')
    plt.xlabel("Time")
    plt.ylabel("Ratio of original to restored network")
    plt.title('Average clustering base on degree centrality') 
    
  
    pos = f.add_subplot(3,2,3) 
    plt.scatter(time_list, cc_ef, s=70, c='deeppink', marker='o')
    plt.xlabel("Time")
    plt.ylabel("Ratio of original to restored network")
    plt.title('Efficiency base on closeness centrality') 
    

    pos = f.add_subplot(3,2,4) 
    plt.scatter(time_list, cc_ac, s=70, c='deeppink', marker='o')
    plt.xlabel("Time")
    plt.ylabel("Ratio of original to restored network")
    plt.title('Average clustering base on closeness centrality') 
    

    pos = f.add_subplot(3,2,5) 
    plt.scatter(time_list, bc_ef, s=70, c='deeppink', marker='o')
    plt.xlabel("Time")
    plt.ylabel("Ratio of original to restored network")
    plt.title('Efficiency base on betweenness_centrality') 
    
    pos = f.add_subplot(3,2,6) 
    plt.scatter(time_list, bc_ac, s=70, c='deeppink', marker='o')
    plt.xlabel("Time")
    plt.ylabel("Ratio of original to restored network")
    plt.title('Average clustering base on betweenness_centrality') 
