import igraph

clics_graph = igraph.read("../output/clics_subgraph.gml")
w2v_graph = igraph.read("../output/word2vec_graph.gml")

def get_community_subgraphs(graph):
    communities = graph.community_infomap()
    community_subgraphs = communities.subgraphs()
    return(community_subgraphs)

def get_b_cubed(graph1, graph2):
    subgraphs1 = get_community_subgraphs(graph1)
    subgraphs2 = get_community_subgraphs(graph2)

    precision_scores = []
    recall_scores = []

    for subgraph1 in subgraphs1:
        for node in subgraph1.vs:
            intersection = []
            for other_node in subgraph1.vs:
                subgraph2 = [g for g in subgraphs2 if node["name"] in [node["ID"] for node in g.vs]][0]
                if other_node["name"] in [node["ID"] for node in subgraph2.vs]:
                    intersection.append(other_node)
            precision_scores.append(len(intersection)/len(subgraph1.vs))
            recall_scores.append(len(intersection)/len(subgraph2.vs))

    precision = sum(precision_scores)/len(precision_scores)
    recall = sum(recall_scores)/len(recall_scores)
    f_score = (2 * precision * recall)/(precision + recall)

    return(precision, recall, f_score)

if __name__=="__main__":
    precision, recall, f_score = get_b_cubed(w2v_graph, clics_graph)
    print("precision: " + str(precision))
    print("recall: " + str(recall))
    print("F-score: " + str(f_score))