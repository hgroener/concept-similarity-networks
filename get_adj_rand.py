import igraph
from datetime import datetime

w2v_path = 'output/word2vec_graph.gml'
CLICS_path = 'output/clics_subgraph.gml'
output_file = 'output/adj_rand.txt'
model_type = 'Brown model'

def get_adj_rand(w2v_path, CLICS_path, output_file, model_type):
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

    adj_rand_coefficient = igraph.compare_communities(w2v_clustering, CLICS_clustering_from_w2v, method="adjusted_rand")

    now = datetime.now()

    with open(output_file, "a+") as f:
        f.write("time: " + str(now) + "\nmodel type: " + model_type + "\n")
        f.write("adjusted rand coefficient: " + str(adj_rand_coefficient))

    return(print("adjusted rand coefficient saved to " + output_file + "."))

if __name__=="__main__":
    get_adj_rand(w2v_path,CLICS_path,output_file,model_type)