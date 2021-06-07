import igraph
import get_b_cubed

w2v_path = "output/word2vec_graph.gml"
CLICS_path = "output/clics_subgraph.gml"

def get_assortativity(test_graph, gold_graph):

    gold_subgraphs = get_b_cubed.coms_sgraphs(gold_graph)[1]

    for node in test_graph.vs:
        for n, subgraph in enumerate(gold_subgraphs):
            IDs = [v["ID"] for v in subgraph.vs]
            if node["ID"] in IDs:
                node["corresponding community"] = n
                break
    a = test_graph.assortativity_nominal("corresponding community", directed=False)
    return(a)

if __name__ == "__main__":
    a_CLICS_communities = get_assortativity(w2v_path, CLICS_path)
    a_w2v_communities = get_assortativity(CLICS_path, w2v_path)
    print("Assortativity using CLICS community labels on w2v graph: " + str(a_CLICS_communities) + "\nAssortativity using w2v community labels on CLICS graph: " + str(a_w2v_communities))