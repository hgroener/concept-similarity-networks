import random as rd

import evaluation
import generate_subgraph

clics_path = 'input/CLICS/network-3-families.gml'
clics_subgraph_path = 'output/CLICS/clics_subgraph_EAT.gml'
EAT_path = 'output/EAT/EAT_graph.gml'
EAT_subgraph_path = 'output/EAT/EAT_subgraph_CLICS.gml'

def get_graph_stats(graph):
    com_num = len(graph.community_infomap())
    com_size = len(graph.vs) / com_num
    return((com_num, com_size))

def cut_edges(sg1, sg2):
    com_num1, com_size1 = get_graph_stats(sg1)
    com_num2, com_size2 = get_graph_stats(sg2)
    if com_num1 > com_num2:
        test = sg2
        gold = sg1
    else:
        test = sg1
        gold = sg2

    test_edges = list(test.es)
    rd.shuffle(test_edges)
    test_edges.sort(key=lambda x: x["weight"])

    n = len(test.es) - len(gold.es)
    del_edges = test_edges[:n]
    test.delete_edges(del_edges)
    return((sg1,sg2))

def compare_networks(test_path, gold_path, test_model_type, gold_model_type):
    test_subgraph, gold_subgraph = generate_subgraph.get_subgraphs(test_path, gold_path)
    test_subgraph, gold_subgraph = cut_edges(test_subgraph, gold_subgraph)
    result_dic = evaluation.get_result_dic(test_subgraph, gold_subgraph, test_model_type, gold_model_type)
    return(result_dic)

if __name__=="__main__":
    results = compare_networks(clics_path, EAT_path, "CLICS", "EAT")
    for key in results:
        print(key, results[key])