from gensim.models import KeyedVectors
import csv
import itertools
import scipy
import igraph
from tqdm import tqdm

#creates network from Word2Vec vectors

mapped_concepts_path = "output/w2v/mapped_concepts.tsv"
w2v_vectors = "output/w2v/wv.wordvectors"
edges = "output/w2v/edges.txt"
output_path = "output/w2v/w2v_no_t.gml"
threshold = 0.7

def read_mappings(table):
    print("reading mappings...")
    with open(table) as fd:
        fd.readline()
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        mapped_IDs = {}
        glosses = []
        for token, ID, gloss, d, e in tqdm(rd):
            if ID in mapped_IDs:
                mapped_IDs[ID] = mapped_IDs[ID] + [token]
            else:
                mapped_IDs[ID] = [token]
                glosses.append(gloss)
    return (mapped_IDs, glosses)

# creates edges from Word2Vec vectors, either by taking cosine similarity of mean vectors or by taking highest cosine similarity calculate for word pair mapped to the concept pair
def create_edges(vector_file, vocab, filename, mean_vectors = True):
    vectors = KeyedVectors.load(vector_file)
    edges = []
    print("creating edges...")
    for ID, other_ID in tqdm(itertools.combinations(vocab, 2)):
        if mean_vectors:
            cosine_similarity = 1 - scipy.spatial.distance.cosine(get_mean_vector(ID, vocab, vectors),
                                                                  get_mean_vector(other_ID, vocab, vectors))
        else:
            cosine_similarity = get_highest_sim(vocab[ID], vocab[other_ID], vectors)
        edges.append((ID, other_ID, cosine_similarity))
    print("\nwriting edges to file...")
    with open(filename, 'w') as f:
        for edge in tqdm(edges):
            f.write("%s\n" % str(edge))
    return edges

# calculates cosine similarity between each combination of words between lists, outputs highest value calculated
def get_highest_sim(words, other_words, vectors):
    sims = []
    for word in words:
        for other_word in other_words:
            sim = 1 - scipy.spatial.distance.cosine(vectors[word], vectors[other_word])
            sims.append(sim)

    highest_sim = max(sims)
    return highest_sim


# calcuates mean vector for a list of words
def get_mean_vector(concepticon_ID, vocab, vectors):
    mean_vector = sum([vectors[word] for word in vocab[concepticon_ID]]) / len(vocab[concepticon_ID])
    return mean_vector

# creates igraph network from mapped concepts and calculated edge weights
def create_network(vocab, glosses, weighted_edges, threshold):
    word2vec_graph = igraph.Graph()
    word2vec_graph.add_vertices([key for key in vocab])
    word2vec_graph.vs["ID"] = [key for key in vocab]
    word2vec_graph.vs["word types"] = [", ".join(vocab[key]) for key in vocab]
    word2vec_graph.vs["Gloss"] = glosses
    no_w = []
    w = []
    for edge_tuple in weighted_edges:
        no_w.append((edge_tuple[0], edge_tuple[1]))
        w.append(edge_tuple[2])
    word2vec_graph.add_edges(no_w)
    word2vec_graph.es['weight'] = w
    if threshold:
        below_t = [e for e in word2vec_graph.es if e['weight']<threshold]
        word2vec_graph.delete_edges(below_t)
    #word2vec_graph = norm_weights(word2vec_graph)
    return word2vec_graph

# combines other functions, creates network from Word2Vec vectors and mapped concepts and saves them to a .gml file
def get_gml(mapped_concepts_path, vectors, edges_path, output_file, threshold=0.7):
    print("network generation started.")
    mapped_IDs, glosses = read_mappings(mapped_concepts_path)
    print("mappings read.")
    edges_list = create_edges(vectors, mapped_IDs, edges_path)
    print("edges created.")
    word2vec_network = create_network(mapped_IDs, glosses, edges_list, threshold)
    print("network created.")
    word2vec_network.write_gml(output_file)
    return(print("graph saved to " + output_file))

if __name__=="__main__":
    get_gml(mapped_concepts_path, w2v_vectors, edges, output_path, threshold=threshold)


