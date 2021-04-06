import igraph

clics_graph = "input/CLICS/network-3-families.gml"
w2v_graph = "output/w2v/w2v.gml"
clics_output = "output/CLICS/clics_subgraph.gml"
w2v_output = "output/w2v/w2v_subgraph_clics.gml"

def compare(raw_graph_path, comparison_graph_path):
    raw_graph = igraph.read(raw_graph_path)
    comparison_graph = igraph.read(comparison_graph_path)
    comparison_IDs = [v["ID"] for v in comparison_graph.vs]
    subgraph_nodes= [v for v in raw_graph.vs if v["ID"] in comparison_IDs]
    subgraph = raw_graph.subgraph(subgraph_nodes, implementation="auto")
    return(subgraph)

def get_subgraphs(graph_path1, graph_path2):
    subgraph1 = compare(graph_path1, graph_path2)
    subgraph2 = compare(graph_path2, graph_path1)
    return((subgraph1, subgraph2))

if __name__=='__main__':
    clics_subgraph, w2v_subgraph = get_subgraphs(clics_graph, w2v_graph)
    clics_subgraph.write_gml(clics_output)
    w2v_subgraph.write_gml(w2v_output)