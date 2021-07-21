from get_b_cubed import coms_sgraphs
import igraph

EAT_path = "output/EAT/EAT_graph.gml"
CLICS_path = "input/CLICS/network-3-families.gml"

def get_assortativity(test_graph, gold_graph):

    gold_coms, gold_subgraphs = coms_sgraphs(gold_graph)

    for test_node in test_graph.vs:
        gold_node = list(gold_graph.vs.select(lambda x: x["ID"] == test_node["ID"]))[0]
        gold_id = gold_node.index
        gold_com = gold_coms.membership[gold_id]
        test_node["corresponding community"] = gold_com

    a = test_graph.assortativity_nominal("corresponding community", directed=False)
    return(a)

def get_symmetric_assortativity(test_graph, gold_graph):
    ab = get_assortativity(test_graph, gold_graph)
    ba = get_assortativity(gold_graph, test_graph)
    assortativity = (ab + ba)/2
    return(assortativity)


if __name__ == "__main__":
    EAT = igraph.read(EAT_path)
    CLICS = igraph.read(CLICS_path)
    print("symmetric measure:", get_symmetric_assortativity(EAT, CLICS))

