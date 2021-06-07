import gensim
import csv
import itertools
import scipy
import igraph
from tqdm import tqdm


# In[4]:

mapped_concepts_path = "output/w2v/mapped_concepts.tsv"
w2v_model = "output/w2v/w2v.model"
edges = "output/w2v/edges.txt"
output_path = "output/w2v/w2v.gml"


def read_mappings(table):
    print("reading mappings...")
    with open(table) as fd:
        fd.readline()
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        mapped_IDs = {}
        for token, ID, c, d, e in tqdm(rd):
            if ID in mapped_IDs:
                mapped_IDs[ID] = mapped_IDs[ID] + [token]
            else:
                mapped_IDs[ID] = [token]
    return mapped_IDs


def create_edges(model_file, vocab, filename):
    model = gensim.models.Word2Vec.load(model_file)
    edges = []
    print("creating edges...")
    for ID, other_ID in tqdm(itertools.combinations(vocab, 2)):
        cosine_similarity = 1 - scipy.spatial.distance.cosine(get_mean_vector(ID, vocab, model),
                                                              get_mean_vector(other_ID, vocab, model))
        edges.append((ID, other_ID, cosine_similarity))
    print("\nwriting edges to file...")
    with open(filename, 'w') as f:
        for edge in tqdm(edges):
            f.write("%s\n" % str(edge))
    return edges

def norm_weights(graph):
    weights = [e["weight"] for e in graph.es]
    print("norming weights...")
    #w_max = max(weights)
    #print("maximum: ", w_max)
    #w_norm = [float(w)/w_max for w in tqdm(weights)]
    w_average = sum(weights)/len(weights)
    print("average weight: ", w_average)
    w_norm = [float(w)/w_average for w in tqdm(weights)]
    graph.es["normed weight"] = w_norm
    return graph

def get_mean_vector(concepticon_ID, vocab, model):
    mean_vector = sum([model.wv[word] for word in vocab[concepticon_ID]]) / len(vocab[concepticon_ID])
    return mean_vector


def create_network(vocab, weighted_edges):
    word2vec_graph = igraph.Graph()
    word2vec_graph.add_vertices([key for key in vocab])
    word2vec_graph.vs["ID"] = [key for key in vocab]
    word2vec_graph.vs["word types"] = [", ".join(vocab[key]) for key in vocab]
    no_w = []
    w = []
    for edge_tuple in weighted_edges:
        no_w.append((edge_tuple[0], edge_tuple[1]))
        w.append(edge_tuple[2])
    word2vec_graph.add_edges(no_w)
    word2vec_graph.es['weight'] = w
    word2vec_graph = norm_weights(word2vec_graph)
    return word2vec_graph


def get_gml(mapped_concepts_path, model, edges_path, output_file):
    print("network generation started.")
    mapped_IDs = read_mappings(mapped_concepts_path)
    print("mappings read.")
    edges_list = create_edges(model, mapped_IDs, edges_path)
    print("edges created.")
    word2vec_network = create_network(mapped_IDs, edges_list)
    print("network created.")
    word2vec_network.write_gml(output_file)
    return(print("graph saved to " + output_file))

if __name__=="__main__":
    get_gml(mapped_concepts_path, w2v_model, edges, output_path)
