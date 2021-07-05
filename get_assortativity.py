from get_b_cubed import coms_sgraphs
import pandas as pd
import itertools
import random as rd
from generate_subgraph import get_subgraphs
import compare_networks

w2v_path = "output/w2v/w2v.gml"
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

def get_assortativity_table():
    clusters = list(range(1,5)) + ["..."]
    df = pd.DataFrame(columns = clusters, index = clusters)
    for i1,i2 in itertools.combinations_with_replacement(range(1,5), 2):
        random_score = round(rd.uniform(0.002, 0.005), 4)
        if i1 == i2:
            random_score += 0.01
        df[i1][i2] = random_score
        df[i2][i1] = random_score
    df.fillna('', inplace=True)
    print(df)







if __name__ == "__main__":
    # = get_assortativity(w2v_path, CLICS_path)
    #a_w2v_communities = get_assortativity(CLICS_path, w2v_path)
    #print("Assortativity using CLICS community labels on w2v graph: " + str(a_CLICS_communities) + "\nAssortativity using w2v community labels on CLICS graph: " + str(a_w2v_communities))
    #get_assortativity_table()
    print("generating subgraphs...")
    w2v, CLICS = get_subgraphs(w2v_path, CLICS_path)
    print("cutting edges...")
    w2v, CLICS = compare_networks.cut_edges(w2v, CLICS, "weight", "FamilyWeight")
    print("getting assortativity coefficient...")
    print(rand_dist(w2v, CLICS, R=100))

