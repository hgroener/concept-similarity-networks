import igraph

clics_graph = igraph.read("output/network-3-families.gml")
word2vec_graph = igraph.read("output/word2vec_graph.gml")

if __name__=="__main__":
    word2vec_IDs = [v["name"] for v in word2vec_graph.vs]
    subgraph_nodes= [v for v in clics_graph.vs if v["ID"] in word2vec_IDs]
    clics_subgraph = clics_graph.subgraph(subgraph_nodes, implementation="auto")
    clics_subgraph.write_gml("output/clics_subgraph.gml")
    print("subgraph created.")