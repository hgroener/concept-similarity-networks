import igraph

clics_graph = "output/network-3-families.gml"
word2vec_graph = "output/word2vec_graph_google.gml"
output = "output/clics_subgraph_google.gml"
stats_output = "output/clics_stats.txt"

def get_subgraph(w2v_graph_path, clics_graph_path, output_path):
    w2v_graph = igraph.read(w2v_graph_path)
    clics_graph = igraph.read(clics_graph_path)
    word2vec_IDs = [v["name"] for v in w2v_graph.vs]
    subgraph_nodes= [v for v in clics_graph.vs if v["ID"] in word2vec_IDs]
    clics_subgraph = clics_graph.subgraph(subgraph_nodes, implementation="auto")
    clics_subgraph_num = len(clics_subgraph.community_infomap())
    clics_subgraph_size = len(clics_subgraph.vs)/clics_subgraph_num
    clics_subgraph.write_gml(output_path)
    return(print("CLICS subgraph created.\nNumber of communities: " + str(clics_subgraph_num) + "\nAverage size of communities: " + str(clics_subgraph_size)))

if __name__=='__main__':
    get_subgraph(word2vec_graph, clics_graph, output)