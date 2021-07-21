import igraph
import sys
import random as rd
from tqdm import tqdm
import pandas as pd
import itertools
sys.path.insert(1, '/')

from generate_subgraph import get_subgraphs
from get_b_cubed import get_b_cubed
from pairwise_evaluation import evaluate as get_pairwise
import get_assortativity
from get_adj_rand import get_adj_rand
from get_spearman import get_spearman_graphs
from get_spearman import spearman_sampling
from main import models

w2v_path = "output/w2v/w2v_no_t.gml.gml"
CLICS_path = "input/CLICS/network-3-families.gml"
EAT_path = "output/EAT/EAT_graph.gml"

def get_graph_stats(graph):
    com_num = len(graph.community_infomap())
    com_size = len(graph.vs) / com_num
    return((com_num, com_size))
def get_community_subgraphs(graph):
    communities = graph.community_infomap()
    community_subgraphs = communities.subgraphs()
    return(community_subgraphs)

def get_glossed_weights(graph, w):
    edgelist = graph.get_edgelist()
    weights = graph.es[w]
    ID_weights = {graph.vs[id1]["Gloss"] + ":" + graph.vs[id2]["Gloss"]: weights[i] for i, (id1, id2) in enumerate(edgelist)}
    return ID_weights

def highest_rank_difference(graph1, graph2, w1="weight", w2="weight"):
    gloss_weights1 = get_glossed_weights(graph1, w1)
    gloss_weights2 = get_glossed_weights(graph2, w2)
    common_weights =  {}
    for pair in gloss_weights1:
        reverse_pair = pair.split(":")[1] + (":") + pair.split(":")[0]
        if pair in gloss_weights2:
            common_weights[pair] = (gloss_weights1[pair], gloss_weights2[pair])
        if reverse_pair in gloss_weights2:
            common_weights[pair] = (gloss_weights1[pair], gloss_weights2[reverse_pair])

    sorted1 = sorted(list(common_weights.keys()), key= lambda x: common_weights[x][0], reverse=True)
    sorted2 = sorted(list(common_weights.keys()), key= lambda x: common_weights[x][1], reverse=True)
    ranked1 = {pair:  (common_weights[pair][0], i) for i, pair in enumerate(sorted1)}
    ranked2 = {pair: (common_weights[pair][1], i) for i, pair in enumerate(sorted2)}
    diffs = {}
    for pair in common_weights:
        w1 = ranked1[pair][0]
        w2 = ranked2[pair][0]
        r1 = ranked1[pair][1]
        r2 = ranked2[pair][1]
        diff  = abs(r1  - r2)
        diffs[pair] = {"w1": w1, "w2": w2, "r1": r1, "r2": r2, "diff": diff}
    top5 = sorted(list(diffs.keys()), key= lambda x: diffs[x]["diff"], reverse=True)[:5]
    #rank_difs = [key + " | " + str(diffs[key]["r1"]) + " - " + str(diffs[key]["r2"]) + " | " + str(diffs[key]["diff"]) for key in top5]
    return(top5)

# calculate similarity metric with Monte-Carlo p-score
def get_p(test_graph, gold_graph, metric, R = 99, prF = False):
    graph_IDs = test_graph.vs["ID"]
    if prF:
        actual_score = metric(test_graph, gold_graph)["F-score"]
    else:
        actual_score = metric(test_graph, gold_graph)
    scores = []
    test_graph_rd = test_graph.copy()
    for i in tqdm(range(R)):
        rd.shuffle(graph_IDs)
        test_graph_rd.vs["ID"] = graph_IDs
        if prF:
            score = metric(test_graph_rd, gold_graph)["F-score"]
        else:
            score = metric(test_graph_rd, gold_graph)
        scores.append(score)
    print("scores for random distributions:", scores)
    S = len([s for s in scores if s > actual_score])
    p = (S + 1)/(R + 1)
    return(actual_score, p)

#cut lowest-weight edges from the network with more edges until both networks have the same number of edges
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

#calculate all metrics for a pair of graphs without p-values
def get_result_dic(test_graph, gold_graph, test_model_type, gold_model_type, test_w = "weight", gold_w = "weight", b_cubed = True, pe = True, adj_rand = True, assortativity = True, spearman = True, nodes = False, edges = False, sample = False):

    test_sg, gold_sg = get_subgraphs(test_graph, gold_graph)
    result_dic = {}

    result_dic["test model"] = test_model_type
    result_dic["gold model"] = gold_model_type

    if spearman:
        if sample:
            result_dic["spearman correlation"] = spearman_sampling(test_sg, gold_sg, w1=test_w, w2=gold_w)
        else:
            result_dic["spearman correlation"] = get_spearman_graphs(test_sg, gold_sg, w1=test_w, w2=gold_w)


    test_sg_cut, gold_sg_cut = cut_edges(test_sg, gold_sg,w1=test_w, w2=gold_w)
    if pe:
        result_dic["pairwise evaluation score"] = get_pairwise(test_sg_cut, gold_sg_cut)
    if b_cubed:
        result_dic["B-Cubed score"] = get_b_cubed(test_sg_cut, gold_sg_cut)
    if adj_rand:
        result_dic["Adjusted Rand Coefficient"] = get_adj_rand(test_sg_cut, gold_sg_cut)
    if assortativity:
        result_dic["assortativity score"] = get_assortativity.get_assortativity(test_sg_cut, gold_sg_cut)
    if nodes:
        result_dic["nodes"] = len(test_sg.vs)
    if edges:
        result_dic["edges"] = len(test_sg_cut.es)

    return(result_dic)

#calculate all metrics with p-values for each network in the "models"-dictionary
def get_results_p(models, p_values = True, R=99, get_rank_difs=True):
    results = []
    for (m1, m2) in itertools.combinations([model for model in models if model["compare"]], 2):
        if m1["type"] != m2["type"]:
            print("comparing {0} to {1}".format(m1["name"], m2["name"]))
            g1 = igraph.read(m1["path"])

            g2 = igraph.read(m2["path"])
            sg1, sg2 = get_subgraphs(g1, g2)
            result_dic = {}

            result_dic["model 1"] = m1["name"]
            result_dic["model 2"] = m2["name"]
            if m1["type"] == "w2v":
                result_dic["spearman correlation"] = spearman_sampling(sg1, sg2, w1=m1["weight attribute"], w2=m2["weight attribute"])
            else:
                result_dic["spearman correlation"] = get_spearman_graphs(sg1, sg2, w1=m1["weight attribute"], w2=m2["weight attribute"])

            sg_cut1, sg_cut2 = cut_edges(sg1, sg2, w1=m1["weight attribute"], w2=m2["weight attribute"])
            #number of common nodes and edges that were compared
            result_dic["nodes"] = len(sg1.vs)
            result_dic["edges"] = len(sg_cut1.es)
            if get_rank_difs:
                result_dic["most differently rated pairs"] = highest_rank_difference(sg1, sg2, w1 = m1["weight attribute"], w2 = m2["weight attribute"])
            sg1_IDs = sg_cut1.vs["ID"]
            #calculates metrics for the actual network
            pe_metrics = get_pairwise(sg_cut1, sg_cut2)
            result_dic["pairwise evaluation metrics"] = pe_metrics
            actual_pe = pe_metrics["F-score"]
            b2_metrics = get_b_cubed(sg_cut1, sg_cut2)
            result_dic["B-cubed metrics"] = b2_metrics
            actual_b2 = b2_metrics["F-score"]
            actual_ar= get_adj_rand(sg_cut1, sg_cut2)
            actual_ac = get_assortativity.get_assortativity(sg_cut1, sg_cut2)

            if p_values:
                pe_list  = []
                b2_list = []
                adj_rand_list = []
                ac_list = []
                print("generating random distributions and calculating p-values...")
                for _ in tqdm(range(R)):
                    rd.shuffle(sg1_IDs)
                    sg_cut1.vs["ID"] = sg1_IDs
                    pe = get_pairwise(sg_cut1, sg_cut2)["F-score"]
                    pe_list.append(pe)
                    b2 = get_b_cubed(sg_cut1, sg_cut2)["F-score"]
                    b2_list.append(b2)
                    adj_rand = get_adj_rand(sg_cut1, sg_cut2)
                    adj_rand_list.append(adj_rand)
                    ac = get_assortativity.get_assortativity(sg_cut1, sg_cut2)
                    ac_list.append(ac)

                #calculates p-values for each metric
                pe_p = calculate_p(pe_list, actual_pe, R=R)
                b2_p = calculate_p(b2_list, actual_b2, R=R)
                adj_rand_p = calculate_p(adj_rand_list, actual_ar, R=R)
                ac_p = calculate_p(ac_list, actual_ac, R=R)

                #saves actual scores with p-values to dictionary object
                result_dic["pairwise evaluation score"] = (actual_pe, pe_p)
                result_dic["B-Cubed score"] = (actual_b2, b2_p)
                result_dic["Adjusted Rand Coefficient"] = (actual_ar, adj_rand_p)
                result_dic["assortativity score"] = (actual_ac, ac_p)

            else:
                result_dic["pairwise evaluation score"] = actual_pe
                result_dic["B-Cubed score"] = actual_b2
                result_dic["Adjusted Rand Coefficient"] = actual_ar
                result_dic["assortativity score"] = actual_ac


            results.append(result_dic)

    return(results)


def calculate_p(scores, actual_score, R=99):
    S = len([s for s in scores if s > actual_score])
    p = (S + 1) / (R + 1)
    return(p)

#compares networks to MultiSimLex, thematic relatedness production norms
def eval_network(models, SimLex_path, trn_path, SimLex_csv_path, trn_csv_path):
    SimLex_scores = []
    trn_scores = []
    SimLex_graph = igraph.read(SimLex_path)
    trn_graph = igraph.read(trn_path)
    for model in models:
        if model["compare"]:
            g = igraph.read(model["path"])
            print("comparing {0} to MultiSimLex pairs".format(model["name"]))
            # only uses sampling when comparing Word2Vec networks to MultiSimLex, because Word2Vec networks are the only ones mapped to enough concepts to stay significant under sampling
            if model["type"] == "w2v":
                spearman_SimLex, p_SimLex, edges_SimLex = spearman_sampling(g, SimLex_graph, w1=model["weight attribute"])
            else:
                spearman_SimLex,p_SimLex, edges_SimLex = get_spearman_graphs(g, SimLex_graph, w1=model["weight attribute"])
            print("comparing {0} to thematic relatedness production norm pairs".format(model["name"]))
            spearman_trn, p_trn, edges_trn = get_spearman_graphs(g, trn_graph, w1=model["weight attribute"])
            SimLex_scores.append((model["name"], spearman_SimLex, p_SimLex, edges_SimLex))
            trn_scores.append((model["name"], spearman_trn, p_trn, edges_trn))

    SimLex_df = pd.DataFrame({"network": [name for (name, score, p, edge) in SimLex_scores],
                              "edges compared": [edge for (name, score, p, edge) in SimLex_scores],
                              "Spearman Rank Coefficient": [round(score,4) if isinstance(score,float) else score for (name, score, p, edge) in SimLex_scores],
                              "p-value": [round(p,4) if isinstance(p, float) else p for (name, score, p, edge) in SimLex_scores]})

    trn_df = pd.DataFrame({"network": [name for (name, score, p, edge) in trn_scores],
                              "edges compared": [edge for (name, score, p, edge) in trn_scores],
                              "Spearman Rank Coefficient": [round(score, 4) if isinstance(score, float) else score for (name, score, p, edge) in trn_scores],
                              "p-value": [round(p, 4)  if isinstance(p, float) else p for (name, score, p, edge) in trn_scores]})
    SimLex_df.to_csv(SimLex_csv_path, header="Spearman Correlation to MultiSimLex similarity scores")
    trn_df.to_csv(trn_csv_path, header="Spearman Correlation to thematic relatedness norms")
    return(print("saved MultiSimLex evaluation scores to {0} and thematic relatedness norm evaluation to {1}".format(SimLex_csv_path, trn_csv_path)))


if __name__=="__main__":
    CLICS = igraph.read(CLICS_path)
    EAT = igraph.read(EAT_path)
    result_dic = get_result_dic(CLICS, EAT, "CLICS", "EAT", test_w="FamilyWeight")
    print(result_dic)
