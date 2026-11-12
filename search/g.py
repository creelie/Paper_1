import networkx as nx, subprocess, sys
GR=__file__.replace('g.py','gr')
def gamma(G,mode='c',hb=26):
    G=nx.convert_node_labels_to_integers(G)
    s=f"{G.number_of_nodes()} {G.number_of_edges()} {mode}\n"+"\n".join(f"{a} {b}" for a,b in G.edges())
    out=subprocess.run([GR,str(hb)],input=s,capture_output=True,text=True).stdout
    return int(out.split()[0])
def strong(G,H): return nx.strong_product(G,H)
def direct(G,H): return nx.tensor_product(G,H)
