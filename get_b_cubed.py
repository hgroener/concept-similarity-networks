import igraph

w2v_path = "output/word2vec_graph.gml"
CLICS_path = "output/clics_subgraph.gml"

def get_community_subgraphs(graph):
    communities = graph.community_infomap()
    community_subgraphs = communities.subgraphs()
    return(community_subgraphs)

def get_b_cubed(test_path, gold_path):
    test_graph = igraph.read(test_path)
    gold_graph = igraph.read(gold_path)
    test_subgraphs = get_community_subgraphs(test_graph)
    gold_subgraphs = get_community_subgraphs(gold_graph)

    precision_scores = []
    recall_scores = []

    for test_subgraph in test_subgraphs:
        for node in test_subgraph.vs:
            intersection = []
            for other_node in test_subgraph.vs:
                gold_subgraph = [g for g in gold_subgraphs if node["name"] in [node["ID"] for node in g.vs]][0]
                if other_node["name"] in [node["ID"] for node in gold_subgraph.vs]:
                    intersection.append(other_node)
            precision_scores.append(len(intersection)/len(test_subgraph.vs))
            recall_scores.append(len(intersection)/len(gold_subgraph.vs))


    result_dic = {}
    result_dic["precision"] = sum(precision_scores)/len(precision_scores)
    result_dic["recall"] = sum(recall_scores)/len(recall_scores)
    result_dic["F-score"] = (2 * result_dic["precision"] * result_dic["recall"])/(result_dic["precision"] + result_dic["recall"])

    return((result_dic))

if __name__=="__main__":
    result_dic = get_b_cubed(w2v_path, CLICS_path)
    for key in result_dic:
        print(key + ": " + str(result_dic[key]))

