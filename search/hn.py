import networkx as nx, sys, time
from g import gamma
def H(N):
    G=nx.Graph(); G.add_nodes_from(range(N))
    G.add_edges_from((u,v) for u in range(N) for v in range(u+1,N) if (v-u)%3==1); return G
O=nx.complete_multipartite_graph(2,2,2)
for N in range(14,17):
    t=time.time(); print(N, gamma(H(N)), gamma(nx.strong_product(O,H(N)),'c',28), round(time.time()-t,1), flush=True)
