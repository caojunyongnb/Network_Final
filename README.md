# Proposal

### Recognition and Vulnerability Analysis of Key Nodes in Power Grid

This study aims to carry out vulnerability analysis and recognize the key nodes in power grid from a complex network perspective. Firstly, a cascading failing model together with different node-attack strategies will be established. Then we propose the electrical centrality measure[1] and compare it with other centrality measures regarding ability to identity critical nodes. Simulations will be subsequently carried on in case studies (e.g. IEEE 30-bus dataset) to verify the accuracy of proposed metrics.

[1] Liu, Bin, et al. "Recognition and vulnerability analysis of key nodes in power grid based on complex network centrality." IEEE Transactions on Circuits and Systems II: Express Briefs 65.3 (2017): 346-350.

[2] Wang, Zhifang, Anna Scaglione, and Robert J. Thomas. "Electrical centrality measures for electric power grid vulnerability analysis." 49th IEEE conference on decision and control (CDC). IEEE, 2010.

[3] Srivastava, Anurag K., et al. "Graph-theoretic algorithms for cyber-physical vulnerability analysis of power grid with incomplete information." Journal of Modern Power Systems and Clean Energy 6.5 (2018): 887-899.

[4] Cetinay, Hale, Karel Devriendt, and Piet Van Mieghem. "Nodal vulnerability to targeted attacks in power grids." Applied network science 3.1 (2018): 1-19.

# Data

SNAP repository https://snap.stanford.edu/data/

UCI Network Data Repository https://networkdata.ics.uci.edu/

Network Repository https://networkrepository.com/

Netzschleuder https://networks.skewed.de/

# Idea

1. replicate 
2. cluster detection????( such as if this is some country data, can we detect the city)

























































































## Nope



1. Attack the network from two perspective

   1. node

      calculate the centrality[1] [2], and try different attack stratigies

      For the node, we can take the node type into account, such as generator load, costume(but not too much, lets check the data)

   2. edges

      calculate the load[2], try diff stratigies( There may be some wronng with the stratigy of SPC.Have asked the author)
      
      '''this is sample so do this First!!!!!!!!!'''
      
      

2. Evaluate the damage.

   1. maximum connected graph (this is feasible)
   2. load model and do the iteration, the [2] load model is much more sample, so we use this  
   3. *Vulnerability Index*[1]
3. The paper just show the final status of the network. However, the collapse of power system is a dynamic process, So we can show the iteration process.  Therefore, the recovery can focus on how to slow down the collapse process. 
<img width="227" alt="image" src="https://user-images.githubusercontent.com/48615762/206497566-cdd157db-e57b-4dd1-a0a9-3d24b0c3cb8c.png">


[1]. Recognition and culnerability

[2]. Western United States power grid]

[3] electrical centrality measures
