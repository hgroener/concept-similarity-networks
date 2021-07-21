# generates subgraphs containing only common nodes given two graphs

import igraph

CLICS_path = "input/CLICS/graphs/network-3-families.gml"
w2v_path = "output/w2v/w2v_no_t.gml"


def compare(raw_graph, comparison_graph):

    comparison_IDs = [v["ID"] for v in comparison_graph.vs]
    subgraph_nodes= [v for v in raw_graph.vs if v["ID"] in comparison_IDs]
    subgraph = raw_graph.subgraph(subgraph_nodes, implementation="auto")
    return(subgraph)

def get_subgraphs(graph1, graph2):
    subgraph1 = compare(graph1, graph2)
    subgraph2 = compare(graph2, graph1)
    return((subgraph1, subgraph2))

if __name__=='__main__':
    CLICS = igraph.read(CLICS_path)
    w2v = igraph.read(w2v_path)
    CLICS_subgraph, w2v_subgraph = get_subgraphs(CLICS, w2v)
    print("number of nodes remaining in CLICS subgraph:", len(CLICS_subgraph.vs))
    print("number of nodes remaining in Word2Vec subgraph:", len(w2v_subgraph.vs))