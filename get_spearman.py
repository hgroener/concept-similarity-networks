from scipy import stats
import igraph
import random as rd
import pandas as pd
from tqdm import tqdm
from generate_subgraph import get_subgraphs

w2v_path = "output/w2v/w2v_subgraph_clics.gml"
EAT_path = "output/EAT/EAT_graph.gml"
CLICS_path_input = "input/CLICS/network-3-families.gml"
CLICS_path = "output/CLICS/clics_subgraph.gml"
languages = ["english", "russian", "chinese", "cantonese", "arabic", "spanish", "polish", "french", "estonian", "finnish"]

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

def get_ID_weights(graph, w):
    edgelist = graph.get_edgelist()
    weights = graph.es[w]
    ID_weights = {graph.vs[id1]["ID"] + ":" + graph.vs[id2]["ID"]: weights[i] for i, (id1, id2) in enumerate(edgelist)}
    return ID_weights



def get_spearman_edges(edges, graph, weight = "weight", sampling=False, n=10):
    # takes list of weighted edges (MultiSimLex) and Graph, returns Spearman ranked coefficient between the edge weights and the length of common edges
    w1 = []
    w2 = []
    edgelist = graph.get_edgelist()
    weights = graph.es[weight]
    edge_IDs = {graph.vs[id1]["ID"] + ":" + graph.vs[id2]["ID"]: weights[i] for i, (id1, id2) in enumerate(edgelist)}
    for (cidA, cidB, w) in edges:
        append = False
        cidA_cidB = cidA + ":" + cidB
        cidB_cidA = cidB + ":" + cidA
        if cidA_cidB in edge_IDs:
            graph_w = edge_IDs[cidA_cidB]
            append = True
        elif cidB_cidA in edge_IDs:
            graph_w = edge_IDs[cidB_cidA]
            append = True
        if append:
            w1.append(w)
            w2.append(graph_w)
    assert len(w1) == len(w2)
    spearman = stats.spearmanr(w1, w2)
    return((spearman, len(w1)))



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


def spearman_sampling(graph1, graph2, w1 = "weight", w2 = "weight", n = 100):
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



def get_central_nodes(graph, w="weight"):
    w_degrees = igraph.Graph.strength(graph, weights=w)
    graph.vs["degree"] = w_degrees
    max_degrees = sorted(graph.vs, key=lambda x:x["degree"], reverse=True)[:5]
    for i, v in enumerate(max_degrees):
        print(i+1, "{0}\ndegree: {1}".format(v["Gloss"], v["degree"]))



if __name__ == "__main__":
    #g1 = igraph.read("output/w2v/w2v_no_t.gml")
    #edges = create_simlex_network(languages, return_graph=False)
    #print(get_spearman_edges(edges, g1))
    #g2 = igraph.read(CLICS_path)
    #print(get_spearman(g1, g2, w2="LanguageWeight", weighted_degrees=True))
    w2v = igraph.read("output/w2v/w2v_no_t.gml")
    CLICS = igraph.read(CLICS_path_input)
    EAT = igraph.read(EAT_path)
    w2v, CLICS = get_subgraphs(w2v, CLICS)
    #get_central_nodes(CLICS, w="FamilyWeight")
    #print(highest_rank_difference(CLICS, EAT, w1="FamilyWeight"))
    #print(get_spearman_graphs(CLICS, EAT, w1="FamilyWeight", no_used_IDs=True))
    print(spearman_sampling(w2v, CLICS, w2="FamilyWeight"))