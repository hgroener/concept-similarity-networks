from scipy import stats
import igraph
import random as rd
from tqdm import tqdm

w2v_path = "output/w2v/w2v_subgraph_clics.gml"
EAT_path = "output/EAT/EAT_graph.gml"
CLICS_path_input = "input/CLICS/network-3-families.gml"
CLICS_path = "output/CLICS/clics_subgraph.gml"
languages = ["english", "russian", "chinese", "cantonese", "arabic", "spanish", "polish", "french", "estonian", "finnish"]


def get_ID_weights(graph, w):
    edgelist = graph.get_edgelist()
    weights = graph.es[w]
    ID_weights = {graph.vs[id1]["ID"] + ":" + graph.vs[id2]["ID"]: weights[i] for i, (id1, id2) in enumerate(edgelist)}
    return ID_weights


# calculates Spearman correlation for two graphs
def get_spearman_graphs(graph1, graph2, w1 = "weight", w2 = "weight"):
    ID_weights1 = get_ID_weights(graph1, w1)
    ID_weights2 = get_ID_weights(graph2, w2)

    edge_weights1 = []
    edge_weights2 = []

    for pair in ID_weights1:
        append = False

        ID1, ID2 = pair.split(":")
        edge_weight1 = ID_weights1[pair]
        reverse_pair = ID2 + ":" +  ID1
        if pair in ID_weights2:
            edge_weight2 = ID_weights2[pair]
            append = True
        elif reverse_pair in ID_weights2:
            edge_weight2 = ID_weights2[reverse_pair]
            append = True
        if append:
            edge_weights1.append(edge_weight1)
            edge_weights2.append(edge_weight2)
    spearman, p = stats.spearmanr(edge_weights1, edge_weights2)
    return(spearman, p, len(edge_weights1))

# calculates Spearman correlation of two graphs on n samples of edges that contain each concepts one time max
def spearman_sampling(graph1, graph2, w1 = "weight", w2 = "weight", n = 100):

    #determines which graph should be iterated over to find common edges. The graph containing less edges is chosen to minimize effort
    if len(graph1.es) < len(graph2.es):
        ID_weights1 = get_ID_weights(graph1, w1)
        ID_weights2 = get_ID_weights(graph2, w2)
    else:
        ID_weights1 = get_ID_weights(graph2, w2)
        ID_weights2 = get_ID_weights(graph1, w1)

    keys_1 = list(ID_weights1.keys())


    spearman_scores = []
    p_values = []


    for i in tqdm(range(n)):
        rd.shuffle(keys_1)
        used_IDs = []
        edge_weights1 = []
        edge_weights2 = []
        for pair in keys_1:
            append = False

            ID1, ID2 = pair.split(":")
            ID_used = (ID1 in used_IDs or ID2 in used_IDs)
            used_IDs += ID1, ID2
            edge_weight1 = ID_weights1[pair]
            reverse_pair = ID2 + ":" +  ID1
            if pair in ID_weights2:
                edge_weight2 = ID_weights2[pair]
                append = True
            elif reverse_pair in ID_weights2:
                edge_weight2 = ID_weights2[reverse_pair]
                append = True
            if append and not ID_used:
                edge_weights1.append(edge_weight1)
                edge_weights2.append(edge_weight2)

        spearman, p = stats.spearmanr(edge_weights1, edge_weights2)
        if p < 0.05:
            spearman_scores.append(spearman)
            p_values.append(p)
    if len(spearman_scores) > 0:
        full_spearman = sum(spearman_scores)/len(spearman_scores)
        average_p = sum(p_values)/len(p_values)
        return(full_spearman, average_p, len(edge_weights1))
    else:
        return("not significant", "> 0.05", len(edge_weights1))



if __name__ == "__main__":

    CLICS = igraph.read(CLICS_path_input)
    EAT = igraph.read(EAT_path)

    print(get_spearman_graphs(EAT, CLICS, w2="FamilyWeight"))