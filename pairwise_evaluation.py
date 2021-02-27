import igraph

clics_graph = igraph.read("output/clics_subgraph.gml")
word2vec_graph = igraph.read("output/word2vec_graph.gml")

if __name__=="__main__":
    word2vec_ID_pairs = [[edge.vertex_tuple[0]["name"],edge.vertex_tuple[1]["name"]] for edge in word2vec_graph.es]
    clics_ID_pairs = [[edge.vertex_tuple[0]["ID"],edge.vertex_tuple[1]["ID"]] for edge in clics_graph.es]

    tp = [edge for edge in word2vec_ID_pairs if edge in clics_ID_pairs]
    fp = [edge for edge in word2vec_ID_pairs if not edge in clics_ID_pairs]
    fn = [edge for edge in clics_ID_pairs if not edge in word2vec_ID_pairs]

    precision = len(tp)/len(word2vec_ID_pairs)
    recall = len(tp)/len(tp+fn)
    f_score = (2 * precision * recall)/(precision + recall)

    print("precision: " + str(precision)+ "\nrecall: " + str(recall) + "\nf-score: " + str(f_score))


