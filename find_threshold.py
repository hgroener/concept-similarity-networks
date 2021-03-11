import create_network
import get_b_cubed

from pathlib import Path
from tqdm import tqdm

model_type = 'Brown Model'
model_path = 'output/word2vec.model'
edges_path = 'output/edges.txt'
shared_concepts_path = 'output/shared_concepts.tsv'
subgraph_path = 'output/clics_subgraph.gml'
result_path_b2 = "output/b_cubed.txt"

threshold = [0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99]

if __name__=="__main__":
    Path("output/w2v_networks").mkdir(parents=True, exist_ok=True)
    for t in tqdm(threshold):
        w2v_gml_path = 'output/w2v_networks/w2v_t' + str(t)[2:] + ".gml"
        w2v_gml_file_path = Path(w2v_gml_path)
        if not w2v_gml_file_path.is_file():
            create_network.get_gml(shared_concepts_path, model_path, edges_path, t, w2v_gml_path)
        get_b_cubed.get_b_cubed(w2v_gml_path, subgraph_path, model_type, result_path_b2, t)