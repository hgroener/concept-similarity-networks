import igraph
import sys
import random as rd
sys.path.insert(1, '/')

from generate_subgraph import get_subgraphs
from get_b_cubed import get_b_cubed
from pairwise_evaluation import evaluate as get_pairwise
from get_assortativity import get_assortativity
from get_adj_rand import get_adj_rand
from get_spearman import get_spearman_graphs


w2v_path = "output/w2v/w2v_subgraph_clics.gml"
CLICS_path = "output/CLICS/clics_subgraph.gml"
model_type = "CLICS"
threshold = "0.96"
output_file = "output/w2v/evaluation.txt"

def get_graph_stats(graph):
    com_num = len(graph.community_infomap())
    com_size = len(graph.vs) / com_num
    return((com_num, com_size))
def get_community_subgraphs(graph):
    communities = graph.community_infomap()
    community_subgraphs = communities.subgraphs()
    return(community_subgraphs)

def get_p(test_graph, gold_graph, metric, R = 10):
    graph_IDs = test_graph.vs["ID"]
    actual_a = metric(test_graph, gold_graph)
    a_scores = []
    test_graph_rd = test_graph.copy()
    for i in tqdm(range(R)):

        rd.shuffle(graph_IDs)
        test_graph_rd.vs["ID"] = graph_IDs
        a = get_assortativity(test_graph_rd, gold_graph)
        a_scores.append(a)
    print("assortativity scores for random distributions:", a_scores)
    S = len([score for score in a_scores if score > actual_a])
    p = (S + 1)/(R + 1)
    return(actual_a, p)

def cut_edges(sg1, sg2, w1="weight", w2="weight"):
    com_num1, com_size1 = get_graph_stats(sg1)
    com_num2, com_size2 = get_graph_stats(sg2)
    if com_num1 > com_num2:
        test = sg2
        w = w2
        gold = sg1
    else:
        test = sg1
        w = w1
        gold = sg2

    test_edges = list(test.es)
    rd.shuffle(test_edges)
    test_edges.sort(key=lambda x: x[w])

    n = len(test.es) - len(gold.es)
    del_edges = test_edges[:n]
    test.delete_edges(del_edges)
    return((sg1,sg2))


def get_result_dic(test_graph, gold_graph, test_model_type, gold_model_type, test_w = "weight", gold_w = "weight", b_cubed = True, pe = True, adj_rand = True, assortativity = True, spearman = True, nodes = False, edges = False):

    test_sg, gold_sg = get_subgraphs(test_graph, gold_graph)
    result_dic = {}

    result_dic["test model"] = test_model_type
    result_dic["gold model"] = gold_model_type
    if pe:
        result_dic["pairwise evaluation score"] = get_pairwise(test_sg, gold_sg)
    if spearman:
        result_dic["spearman correlation"] = get_spearman_graphs(test_sg, gold_sg, w1=test_w, w2=gold_w)


    test_sg_cut, gold_sg_cut = cut_edges(test_sg, gold_sg,w1=test_w, w2=gold_w)
    if b_cubed:
        result_dic["B-Cubed score"] = get_b_cubed(test_sg_cut, gold_sg_cut)
    if adj_rand:
        result_dic["Adjusted Rand Coefficient"] = get_adj_rand(test_sg_cut, gold_sg_cut)
    if assortativity:
        result_dic["assortativity score"] = get_assortativity(test_sg_cut, gold_sg_cut)
    if nodes:
        result_dic["nodes"] = len(test_sg.vs)
    if edges:
        result_dic["edges"] = len(test_sg_cut.es)

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