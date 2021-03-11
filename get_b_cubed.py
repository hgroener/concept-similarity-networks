import igraph
from datetime import datetime

clics_graph = "output/clics_subgraph.gml"
w2v_graph = "output/word2vec_graph.gml"
model_type = "Brown model"
output_file = "output/b_cubed.txt"
threshold = 0.97

def get_community_subgraphs(graph):
    communities = graph.community_infomap()
    community_subgraphs = communities.subgraphs()
    return(community_subgraphs)

def get_results(graph_path1, graph_path2):
    graph1 = igraph.read(graph_path1)
    graph2 = igraph.read(graph_path2)
    subgraphs1 = get_community_subgraphs(graph1)
    subgraphs2 = get_community_subgraphs(graph2)

    subgraph1_num = len(subgraphs1)
    subgraph1_size = len(graph1.vs)/subgraph1_num

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

    result_dic = {}
    result_dic["communities"] = subgraph1_num
    result_dic["average community size"] = subgraph1_size
    result_dic["precision"] = sum(precision_scores)/len(precision_scores)
    result_dic["recall"] = sum(recall_scores)/len(recall_scores)
    result_dic["F-Score"] = (2 * result_dic["precision"] * result_dic["recall"])/(result_dic["precision"] + result_dic["recall"])

    return((result_dic))

def get_b_cubed(graph_path1, graph_path2, model_type, output_file, threshold):
    result_dic = get_results(graph_path1, graph_path2)
    now = datetime.now()
    with open(output_file, "a+") as f:
        f.write("time: " + str(now) + "\nmodel type: " + model_type + "\nthreshold: " + str(threshold) + "\n")
        for key in result_dic:
            f.write(key + ": " + str(result_dic[key]) + "\n")
        f.write("\n\n")
    return(print("\nB-Cubed scores saved to " + output_file))

if __name__=="__main__":
    get_b_cubed(w2v_graph, clics_graph, model_type, output_file, threshold)

