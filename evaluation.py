import igraph
import sys
sys.path.insert(1, '/')

import get_b_cubed
import pairwise_evaluation
import get_assortativity
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

def get_result_dic(test_graph, gold_graph, test_model_type, gold_model_type, b_cubed = True, pe = True, adj_rand = True, assortativity = True):

    result_dic = {}

    result_dic["test model"] = test_model_type
    result_dic["gold model"] = gold_model_type

    if b_cubed == True:
        result_dic["B-Cubed score"] = get_b_cubed.get_b_cubed(test_graph, gold_graph)
    if pe == True:
        result_dic["pairwise evaluation score"] = pairwise_evaluation.evaluate(test_graph, gold_graph)
    if adj_rand == True:
        result_dic["Adjusted Rand Coefficient"] = get_adj_rand.get_adj_rand(test_graph, gold_graph)
    if assortativity == True:
        result_dic["assortativity score"] = get_assortativity.get_assortativity(test_graph, gold_graph)

    return(result_dic)

def evaluate(test_graph, gold_graph, model_type, threshold, output_file):
    result_dic = get_result_dic(test_graph, gold_graph, model_type, threshold)
    with open(output_file, "a+") as f:
        for key in result_dic:
            f.write(key + ": " + str(result_dic[key]) + "\n")
        f.write("\n\n")
    return(print("\nevaluation results saved to " + output_file + "."))


if __name__=="__main__":
    w2v_graph = igraph.read(w2v_path)
    CLICS_graph = igraph.read(CLICS_path)
    evaluate(w2v_graph, CLICS_graph, model_type, threshold, output_file)