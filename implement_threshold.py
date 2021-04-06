import igraph

w2v_path = "output/w2v/w2v.gml"
threshold = 0.98

def implement_threshold(w2v_graph, threshold):
    edgelist = []
    for edge in w2v_graph.es:
        if edge["weight"]<threshold:
            edgelist.append(edge)
    w2v_graph.delete_edges(edgelist)
    return(w2v_graph)

if __name__=="__main__":
    w2v_graph = igraph.read(w2v_path)
    igraph.summary(w2v_graph_raw)
    w2v_graph_t = implement_treshold(w2v_graph, threshold)
    igraph.summary(w2v_graph_t)