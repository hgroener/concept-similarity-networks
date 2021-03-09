import word2vecmodel
import mapping
import create_network
import generate_subgraph
import pairwise_evaluation
import get_b_cubed

corpus_path = 'D:/Brown/brown.csv'
model_path = 'output/word2vec.model'
vocab_path = 'output/model_vocab.txt'
shared_concepts_path = 'output/shared_concepts.tsv'
edges_path = 'output/edges.txt'
threshold = 0.97
w2v_gml_path = 'output/word2vec_graph.gml'
clics_gml_path = 'output/network-3-families.gml'
subgraph_output_path = 'output/clics_subgraph.gml'

if __name__=="__main__":
    word2vecmodel.build_model(corpus_path, model_path, vocab_path)
    mapping.get_shared_concepts(vocab_path, shared_concepts_path)
    create_network.get_gml(shared_concepts_path, model_path, edges_path, threshold, w2v_gml_path)
    generate_subgraph.get_subgraph(w2v_gml_path, clics_gml_path, subgraph_output_path)
    pairwise_evaluation.evaluate(subgraph_output_path, w2v_gml_path)
    get_b_cubed.get_b_cubed(w2v_gml_path, subgraph_output_path)