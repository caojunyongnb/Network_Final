from with_null_model import graph_compare
import numpy as np

def get_all_graph(theta,T):
    gc = graph_compare('power-US-Grid.mtx', theta=theta, T=T)
    result = gc.attack_three_graph()
    return result
def draw_(Graph, y_log_flag=False, x_log_flag=False, cols=30,title=''):
    import matplotlib.pyplot as plt
    d_list = [Graph.degree()[i] for i in dict(Graph.degree).keys()]

    if x_log_flag == False:
        bin_ = np.linspace(0, max(d_list), cols)
        if y_log_flag == False:
            plt.hist(d_list, bins=bin_, density=True)
        elif y_log_flag == True:
            plt.hist(d_list, bins=bin_, log=True, density=True)
    elif x_log_flag == True:
        min_=max([min(d_list),1])
        bin_ = np.logspace(np.log10(min_), np.log10(max(d_list) + 1), cols)
        if y_log_flag == False:
            plt.hist(d_list, bins=bin_, density=True)
        elif y_log_flag == True:
            plt.hist(d_list, bins=bin_, log=True, density=True)
        plt.xlabel("Degree")
        plt.xscale('log')
    plt.xlabel("Degree")
    plt.ylabel("count")

    plt.title(title)
    plt.savefig('Result/' + title + '.png')
    plt.show()

result=get_all_graph(1.2,1.2)
draw_(result['er'][0],y_log_flag=True, x_log_flag=True,title='ER_graph')
draw_(result['ba'][0],y_log_flag=True, x_log_flag=True,title='BA_graph')
draw_(result['us'][0],y_log_flag=True, x_log_flag=True,title='US_Power_grid')

# plt.plot(x, y, "r", marker='*', ms=10, label="a")
# plt.xticks(rotation=45)
# plt.legend(loc="upper left")
# plt.savefig("a.jpg")
# plt.show()
