import igraph

EAT_path = 'output/EAT/EAT_graph.gml'
CLICS_path = 'output/CLICS/clics_subgraph.gml'

def get_adj_rand(test_graph, gold_graph):

    gold_clustering = gold_graph.community_infomap()
    gold_subgraphs = gold_clustering.subgraphs()

    for node in test_graph.vs:
        for n, subgraph in enumerate(gold_subgraphs):
            IDs = [v["ID"] for v in subgraph.vs]
            if node["ID"] in IDs:
                node["corresponding community"] = n
                break

    gold_clustering_from_test = igraph.clustering.VertexClustering.FromAttribute(graph=test_graph, attribute="corresponding community")
    test_clustering = test_graph.community_infomap()

    adj_rand_coefficient = igraph.compare_communities(test_clustering, gold_clustering_from_test, method="adjusted_rand")

    return(adj_rand_coefficient)

if __name__=="__main__":
    EAT = igraph.read(EAT_path)
    CLICS = igraph.read(CLICS_path)
    print(get_adj_rand(EAT,CLICS))