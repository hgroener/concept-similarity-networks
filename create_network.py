import gensim
import csv
import itertools
import scipy
from tqdm import tqdm
import igraph


# In[4]:


def read_mappings(table):
    with open(table) as fd:
        fd.readline()
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        mapped_IDs = {}
        for token, ID, c, d, e in rd:
            if ID in mapped_IDs:
                mapped_IDs[ID] = mapped_IDs[ID] + [token]
            else:
                mapped_IDs[ID] = [token]
    return mapped_IDs


def create_edges(model, vocab, threshold, filename):
    brown_model = gensim.models.Word2Vec.load(model)
    edges = []
    for ID, other_ID in tqdm(itertools.combinations(vocab, 2)):
        cosine_similarity = 1 - scipy.spatial.distance.cosine(get_mean_vector(ID, vocab, brown_model),
                                                              get_mean_vector(other_ID, vocab, brown_model))
        if cosine_similarity > threshold:
            edges.append((ID, other_ID, cosine_similarity))
    print("edges per node:" + str(len(edges) / len(vocab)))
    with open(filename, 'w') as f:
        for edge in edges:
            f.write("%s\n" % str(edge))
    return edges


def get_mean_vector(concepticon_ID, vocab, model):
    mean_vector = sum([model.wv[word] for word in vocab[concepticon_ID]]) / len(vocab[concepticon_ID])
    return mean_vector


def create_network(vocab, weighted_edges):
    word2vec_graph = igraph.Graph()
    word2vec_graph.add_vertices([key for key in vocab])
    word2vec_graph.vs["word types"] = [", ".join(vocab[key]) for key in vocab]
    no_w = []
    w = []
    for edge_tuple in weighted_edges:
        no_w.append((edge_tuple[0], edge_tuple[1]))
        w.append(edge_tuple[2])
    word2vec_graph.add_edges(no_w)
    word2vec_graph.es['weight'] = w
    return word2vec_graph


if __name__ == "__main__":
    mapped_IDs = read_mappings("output/shared_concepts.tsv")
    edges = create_edges("output/brown_model.model", mapped_IDs, 0.97, "output/edges.txt")
    word2vec_network = create_network(mapped_IDs, edges)
    word2vec_network.write_gml("output/word2vec_graph.gml")
