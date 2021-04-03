import word2vecmodel
import mapping
import create_network
import generate_subgraph
import evaluation

from pathlib import Path

Path("output/w2v").mkdir(parents=True, exist_ok=True)

corpus_path = 'Brown/brown.csv'
model_type = 'Brown Model'
model_path = 'output/w2v/word2vec.model'
vocab_path = 'output/w2v/model_vocab.txt'
shared_concepts_path = 'output/w2v/shared_concepts.tsv'
edges_path = 'output/w2v/edges.txt'
threshold = 0.98
w2v_gml_path = 'output/w2v/word2vec_graph.gml'
clics_gml_path = 'output/network-3-families.gml'
w2v_subgraph_output = 'output/w2v/w2v_subgraph.gml'
CLICS_subgraph_output = 'output/w2v/clics_subgraph.gml'
result_path = "output/w2v/evaluation.txt"

if __name__=="__main__":
    word2vecmodel.build_model(corpus_path, model_path, vocab_path)
    mapping.get_shared_concepts(vocab_path, shared_concepts_path)
    create_network.get_gml(shared_concepts_path, model_path, edges_path, threshold, w2v_gml_path)
    generate_subgraph.get_subgraph(w2v_gml_path, clics_gml_path, w2v_subgraph_output)
    generate_subgraph.get_subgraph(clics_gml_path, w2v_gml_path, CLICS_subgraph_output)
    evaluation.evaluate(w2v_subgraph_output, CLICS_subgraph_output, model_type, threshold, result_path)