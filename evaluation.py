import igraph
from datetime import datetime
import pandas
import sys
sys.path.insert(1, '/')

import get_b_cubed
import pairwise_evaluation
import get_assortativity
import get_spearman
import get_adj_rand


w2v_path = "output/w2v/w2v_subgraph_clics.gml"
CLICS_path = "output/CLICS/clics_subgraph.gml"
model_type = "CLICS"
threshold = "0.96"
output_file = "output/w2v/evaluation.txt"

def get_community_subgraphs(graph):
    communities = graph.community_infomap()
    community_subgraphs = communities.subgraphs()
    return(community_subgraphs)

def get_result_dic(test_path, gold_path, model_type, threshold, b_cubed = True, pe = True, adj_rand = True, assortativity = True):

    test_graph = igraph.read(test_path)
    test_coms = get_community_subgraphs(test_graph)

    result_dic = {}
    result_dic["time"] = datetime.now()
    result_dic["model type"] = model_type
    result_dic["threshold"] = threshold
    result_dic["number of communities"] = len(test_coms)
    result_dic["average community size"] = len(test_graph.vs)/len(test_coms)
    result_dic["spearman coefficient"] = get_spearman.get_spearman(test_path, gold_path)
    if b_cubed == True:
        result_dic["B-Cubed score"] = get_b_cubed.get_b_cubed(test_path, gold_path)
    if pe == True:
        result_dic["pairwise evaluation score"] = pairwise_evaluation.evaluate(test_path, gold_path)
    if adj_rand == True:
        result_dic["Adjusted Rand Coefficient"] = get_adj_rand.get_adj_rand(test_path, gold_path)
    if assortativity == True:
        result_dic["assortativity score"] = get_assortativity.get_assortativity(test_path, gold_path)

    return(result_dic)

def evaluate(test_path, gold_path, model_type, threshold, output_file):
    result_dic = get_result_dic(test_path, gold_path, model_type, threshold)
    with open(output_file, "a+") as f:
        for key in result_dic:
            f.write(key + ": " + str(result_dic[key]) + "\n")
        f.write("\n\n")
    return(print("\nevaluation results saved to " + output_file + "."))


if __name__=="__main__":
    evaluate(w2v_path, CLICS_path, model_type, threshold, output_file)