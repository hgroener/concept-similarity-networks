import igraph

w2v_path = "output/word2vec_graph_google.gml"
CLICS_path = "output/clics_subgraph_google.gml"

def evaluate(test_graph, gold_graph):

    test_ID_pairs = [[edge.vertex_tuple[0]["ID"],edge.vertex_tuple[1]["ID"]] for edge in test_graph.es]
    gold_ID_pairs = [[edge.vertex_tuple[0]["ID"],edge.vertex_tuple[1]["ID"]] for edge in gold_graph.es]

    tp = [edge for edge in test_ID_pairs if edge in gold_ID_pairs]
    #fp = [edge for edge in test_ID_pairs if not edge in gold_ID_pairs]
    fn = [edge for edge in gold_ID_pairs if not edge in test_ID_pairs]

    precision = len(tp)/len(test_ID_pairs)
    recall = len(tp)/len(tp+fn)
    if precision + recall > 0:
        f_score = (2 * precision * recall)/(precision + recall)
    else:
        f_score = 0

    return({"precision": precision, "recall": recall, "F-score": f_score})


if __name__=="__main__":
    result_dic = evaluate(w2v_path, CLICS_path)
    for key in result_dic:
        print(key + ": " + str(result_dic[key]))