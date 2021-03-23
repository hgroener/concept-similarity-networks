from scipy import stats
import igraph

w2v_path = "output/word2vec_graph.gml"
CLICS_path = "output/clics_subgraph.gml"

def get_sorted_degrees(graph_path):
    graph = igraph.read(graph_path)
    ID_degree_list = []
    for node in graph.vs:
        ID_degree_list.append((node["ID"], node.degree()))
    sorted_ID_tuples = sorted(ID_degree_list, key=lambda tup: tup[0])
    degrees = [tup[1] for tup in sorted_ID_tuples]
    return(degrees)

def get_spearman(graph_path1, graph_path2):
    degrees1 = get_sorted_degrees(graph_path1)
    degrees2 = get_sorted_degrees(graph_path2)
    spearman = stats.spearmanr(degrees1, degrees2)
    return({"spearman correlation": spearman[0], "p-value": spearman[1]})

if __name__ == "__main__":
    print(get_spearman(w2v_path, CLICS_path))