import igraph

w2v_path = 'output/word2vec_graph.gml'
CLICS_path = 'output/clics_subgraph.gml'

def get_adj_rand(w2v_path, CLICS_path):
    w2v_graph = igraph.read(w2v_path)
    CLICS_graph = igraph.read(CLICS_path)

    CLICS_clustering = CLICS_graph.community_infomap()
    CLICS_subgraphs = CLICS_clustering.subgraphs()

    for node in w2v_graph.vs:
        for n, subgraph in enumerate(CLICS_subgraphs):
            IDs = [v["ID"] for v in subgraph.vs]
            if node["ID"] in IDs:
                node["corresponding community"] = n
                break

    CLICS_clustering_from_w2v = igraph.clustering.VertexClustering.FromAttribute(graph=w2v_graph, attribute="corresponding community")
    w2v_clustering = w2v_graph.community_infomap()

    return(igraph.compare_communities(w2v_clustering, CLICS_clustering_from_w2v, method="adjusted_rand"))

if __name__=="__main__":
    print(get_adj_rand(w2v_path,CLICS_path))