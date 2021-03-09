import igraph

clics_graph = "output/clics_subgraph_google.gml"
word2vec_graph = "output/word2vec_graph_google.gml"

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
    f_score = (2 * precision * recall)/(precision + recall)

    return(print("pairwise evalulation scores:\n" + "precision: " + str(precision)+ "\nrecall: " + str(recall) + "\nf-score: " + str(f_score)))

if __name__=="__main__":
    evaluate(clics_graph, word2vec_graph)