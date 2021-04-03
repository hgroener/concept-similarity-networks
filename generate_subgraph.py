import igraph

clics_graph = "output/network-3-families.gml"
word2vec_graph = "output/word2vec_graph.gml"
output = "output/clics_subgraph.gml"

def get_subgraph(raw_graph_path, comparison_graph_path, output_path):
    raw_graph = igraph.read(raw_graph_path)
    comparison_graph = igraph.read(comparison_graph_path)
    comparison_IDs = [v["ID"] for v in comparison_graph.vs]
    subgraph_nodes= [v for v in raw_graph.vs if v["ID"] in comparison_IDs]
    subgraph = raw_graph.subgraph(subgraph_nodes, implementation="auto")
    subgraph_size = len(subgraph.vs)
    subgraph_com_num = len(subgraph.community_infomap())
    subgraph_com_size = len(subgraph.vs)/subgraph_com_num
    subgraph.write_gml(output_path)
    return(print("Subgraph created.\nNumber of nodes: " + str(subgraph_size) + "\nNumber of communities: " + str(subgraph_com_num) + "\nAverage size of communities: " + str(subgraph_com_size)))

if __name__=='__main__':
    get_subgraph(clics_graph, word2vec_graph, output)