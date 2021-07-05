import random as rd
import igraph

import evaluation
import generate_subgraph
import get_spearman

clics_path = 'input/CLICS/network-3-families.gml'
clics_subgraph_path = 'output/CLICS/clics_subgraph_EAT.gml'
EAT_path = 'output/EAT/EAT_graph.gml'
EAT_subgraph_path = 'output/EAT/EAT_subgraph_CLICS.gml'






def compare_networks(test_path, gold_path, test_model_type, gold_model_type, test_w = "weight", gold_w = "weight", nodes = False, edges = False):
    test_subgraph, gold_subgraph = generate_subgraph.get_subgraphs(test_path, gold_path)
    assert len(test_subgraph.vs) == len(gold_subgraph.vs)
    result_dic = evaluation.get_result_dic(test_subgraph, gold_subgraph, test_model_type, gold_model_type, test_w=test_w, gold_w=gold_w, nodes = nodes, edges = edges)
    return(result_dic)

if __name__=="__main__":
    #results = compare_networks(clics_path, EAT_path, "CLICS", "EAT", test_w = "FamilyWeight")
    # for key in results:
       # print(key, results[key])

    CLICS, EAT = generate_subgraph.get_subgraphs("output/w2v/w2v_no_t.gml", "output/MultiSimLex/MultiSimLex.gml")
    print(get_spearman.get_spearman_graphs(CLICS, EAT))
