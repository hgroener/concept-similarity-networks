from scipy import stats
import igraph

w2v_path = "output/w2v/w2v_subgraph_clics.gml"
CLICS_path = "output/CLICS/clics_subgraph.gml"

def get_sorted_degrees(graph):
    ID_degree_list = []
    for node in graph.vs:
        ID_degree_list.append((node["ID"], node.degree()))
    sorted_ID_tuples = sorted(ID_degree_list, key=lambda tup: int(tup[0]))
    degrees = [tup[1] for tup in sorted_ID_tuples]
    return(degrees)

def get_sorted_weighted_degrees(graph, w):
    w_degrees = igraph.Graph.strength(graph, weights=w)
    graph.vs["WeightedDegree"] = w_degrees
    #vs_sorted_by_degree = sorted(list(graph.vs), key=lambda v: int(v["WeightedDegree"]), reverse=True)
    #for n, v in enumerate(vs_sorted_by_degree):
        #v["WeightedDegreeRank"] = n
    vs_sorted = sorted(list(graph.vs), key=lambda v: int(v["ID"]))
    sorted_w_degrees = [v["WeightedDegree"] for v in vs_sorted]
    return(sorted_w_degrees)

def get_spearman(graph1, graph2, w1="weight", w2="weight", weighted_degrees=False):
    if weighted_degrees:
        degrees1 = get_sorted_weighted_degrees(graph1, w1)
        degrees2 = get_sorted_weighted_degrees(graph2, w2)
    else:
        degrees1 = get_sorted_degrees(graph1)
        degrees2 = get_sorted_degrees(graph2)
    spearman = stats.spearmanr(degrees1, degrees2)
    return(spearman)

if __name__ == "__main__":
    g1 = igraph.read(w2v_path)
    g2 = igraph.read(CLICS_path)
    print(get_spearman(g1, g2, w2="LanguageWeight", weighted_degrees=True))