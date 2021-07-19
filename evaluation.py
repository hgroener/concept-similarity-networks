import igraph
import sys
import random as rd
from tqdm import tqdm
import pandas as pd
sys.path.insert(1, '/')

from generate_subgraph import get_subgraphs
from get_b_cubed import get_b_cubed
from pairwise_evaluation import evaluate as get_pairwise
import get_assortativity
from get_adj_rand import get_adj_rand
from get_spearman import get_spearman_graphs
from get_spearman import spearman_sampling
from get_spearman import get_ID_weights
from main import models

w2v_path = "output/w2v/w2v_subgraph_clics.gml"
CLICS_path = "input/CLICS/network-3-families.gml"
EAT_path = "output/EAT/EAT_graph.gml"
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
    rank_difs = [key + " | " + str(diffs[key]["r1"]) + " - " + str(diffs[key]["r2"]) + " | " + str(diffs[key]["diff"]) for key in top5]
    return(rank_difs)


def get_p(test_graph, gold_graph, metric, R = 10, prF = False):
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

def eval_network(models, SimLex_path, trn_path, SimLex_csv_path, trn_csv_path):
    SimLex_scores = []
    trn_scores = []
    SimLex_graph = igraph.read(SimLex_path)
    trn_graph = igraph.read(trn_path)
    for model in models:
        if model["compare"]:
            g = igraph.read(model["path"])
            print("comparing {0} to MultiSimLex pairs".format(model["name"]))
            if model["type"] == "w2v":
                spearman_SimLex, p_SimLex, edges_SimLex = spearman_sampling(g, SimLex_graph, w1=model["weight attribute"])
                #spearman_trn, p_trn, edges_trn = spearman_sampling(g, trn_graph, w1=model["weight attribute"])
            else:
                spearman_SimLex,p_SimLex, edges_SimLex = get_spearman_graphs(g, SimLex_graph, w1=model["weight attribute"])
            spearman_trn, p_trn, edges_trn = get_spearman_graphs(g, trn_graph, w1=model["weight attribute"])
            #spearman_SimLex, edges_compared = get_spearman_edges(SimLex_edges, igraph.read(model["path"]), weight=model["weight attribute"])
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





def evaluate(test_graph, gold_graph, model_type, threshold, output_file):
    result_dic = get_result_dic(test_graph, gold_graph, model_type, threshold)
    with open(output_file, "a+") as f:
        for key in result_dic:
            f.write(key + ": " + str(result_dic[key]) + "\n")
        f.write("\n\n")
    return(print("\nevaluation results saved to " + output_file + "."))



if __name__=="__main__":
    SimLex = "output/MultiSimLex/MultiSimLex.gml"
    trn = "output/thematic_relatedness/trn.gml"
    SimLex_csv = "evaluation/SimLex_results.csv"
    trn_csv = "evaluation/trn_eval.csv"
    #w2v_graph = igraph.read(w2v_path)
    EAT_graph = igraph.read(EAT_path)
    CLICS_graph = igraph.read(CLICS_path)
    #test_sg, gold_sg = get_subgraphs(EAT_graph, CLICS_graph)
    #eval_network(models, SimLex, trn, SimLex_csv, trn_csv)
    #print(get_p(test_sg, gold_sg, get_adj_rand, R = 10, prF=False))
    #evaluate(w2v_graph, CLICS_graph, model_type, threshold, output_file)
    CLICS, EAT = get_subgraphs(CLICS_graph, EAT_graph)
    #CLICS, EAT = cut_edges(CLICS, EAT, w1="FamilyWeight")
    #print("adj rand CLICS - EAT:", get_adj_rand(CLICS, EAT))
    #print("adj rand EAT - CLICS", get_adj_rand(EAT, CLICS))
    print(highest_rank_difference(CLICS, EAT, w1="FamilyWeight"))