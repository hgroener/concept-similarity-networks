import igraph
from datetime import datetime

clics_graph = "output/clics_subgraph_google.gml"
word2vec_graph = "output/word2vec_graph_google.gml"
model_type = "pretrained Google vectors"
output_file = "output/pairwise_evaluation.txt"


def evaluate(clics_graph_path, w2v_graph_path):
    clics_graph = igraph.read(clics_graph_path)
    w2v_graph = igraph.read(w2v_graph_path)
    word2vec_ID_pairs = [[edge.vertex_tuple[0]["name"],edge.vertex_tuple[1]["name"]] for edge in w2v_graph.es]
    clics_ID_pairs = [[edge.vertex_tuple[0]["ID"],edge.vertex_tuple[1]["ID"]] for edge in clics_graph.es]

    tp = [edge for edge in word2vec_ID_pairs if edge in clics_ID_pairs]
    #fp = [edge for edge in word2vec_ID_pairs if not edge in clics_ID_pairs]
    fn = [edge for edge in clics_ID_pairs if not edge in word2vec_ID_pairs]

    precision = len(tp)/len(word2vec_ID_pairs)
    recall = len(tp)/len(tp+fn)
    if precision + recall > 0:
        f_score = (2 * precision * recall)/(precision + recall)
    else:
        f_score = 0
    #print("pairwise evalulation scores:\n" + "precision: " + str(precision) + "\nrecall: " + str(recall) + "\nf-score: " + str(f_score))
    return({"precision": precision, "recall": recall, "F-Score": f_score})

def pairwise_evaluation(clics_graph, w2v_graph, model_type, output_file):
    result_dic = evaluate(clics_graph, w2v_graph)
    now = datetime.now()
    with open(output_file, "a+") as f:
        f.write("time: " + str(now) + "\nmodel type: " + model_type + "\n")
        for key in result_dic:
            f.write(key + ": " + str(result_dic[key]) + "\n")
        f.write("\n\n")
    return(print("pairwise evaluation scores saved to " + output_file))

if __name__=="__main__":
    pairwise_evaluation(clics_graph, word2vec_graph, model_type, output_file)