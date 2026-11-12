import sys; sys.path.insert(0,'.'); from g import gamma; import networkx as nx, subprocess, itertools, pickle
from networkx.generators.atlas import graph_atlas_g
def twinfree(G):
    N={v:frozenset(G[v])|{v} for v in G}; return len(set(N.values()))==len(N)
cands=[G for G in graph_atlas_g() if 4<=G.number_of_nodes()<=7 and nx.is_connected(G) and twinfree(G) and not nx.is_forest(G)]
gam=[gamma(G) for G in cands]
print(len(cands),file=sys.stderr)
pickle.dump((cands,gam),open('cands.pkl','wb'))
pairs=[]; blocks=[]
for i in range(len(cands)):
    for j in range(i,len(cands)):
        G,H=cands[i],cands[j]
        if G.number_of_nodes()*H.number_of_nodes()>49: continue
        P=nx.convert_node_labels_to_integers(nx.strong_product(G,H)); n=P.number_of_nodes()
        A=nx.to_numpy_array(P,dtype=int)
        blocks.append(f"{n} {gam[i]*gam[j]}\n"+"\n".join(''.join(map(str,r)) for r in A))
        pairs.append((i,j))
pickle.dump(pairs,open('pairs.pkl','wb'))
print(len(pairs),file=sys.stderr)
open('blocks.txt','w').write("\n".join(blocks)+"\n")
