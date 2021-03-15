import create_network
import get_b_cubed

import igraph
from pathlib import Path
from tqdm import tqdm

model_type = 'Brown Model'
model_path = 'output/word2vec.model'
edges_path = 'output/edges.txt'
shared_concepts_path = 'output/shared_concepts.tsv'
subgraph_path = 'output/clics_subgraph.gml'
result_path_b2 = "output/b_cubed.txt"
threshold = [0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99]

clics_subgraph = igraph.read(subgraph_path)
clics_subgraph_num = len(clics_subgraph.community_infomap())
clics_subgraph_size = len(clics_subgraph.vs) / clics_subgraph_num

def find_threshold(model_type, model_path, edges_path, shared_concepts_path, CLICS_subgraph_path, result_path_b2, threshold_list):
    Path("output/w2v_networks").mkdir(parents=True, exist_ok=True)
    results = []
    for t in tqdm(threshold_list):
        w2v_gml_path = 'output/w2v_networks/w2v_t' + str("{:.2f}".format(t))[2:] + ".gml"
        w2v_gml_file_path = Path(w2v_gml_path)
        if not w2v_gml_file_path.is_file():
            create_network.get_gml(shared_concepts_path, model_path, edges_path, t, w2v_gml_path)
        result_dic = get_b_cubed.get_b_cubed(w2v_gml_path, CLICS_subgraph_path, model_type, result_path_b2, t, return_scores=True)
        results.append(result_dic)
    closest_com_num_dif = clics_subgraph_num
    closest_com_size_dif = clics_subgraph_size
    highest_spearman_c = -1
    for (n,dic) in enumerate(results):
        com_num = dic["communities"]
        com_num_dif = abs(com_num - clics_subgraph_num)
        if com_num_dif < closest_com_num_dif:
            closest_com_num = com_num
            closest_com_num_dif = com_num_dif
            best_t_by_com_num = threshold_list[n]
        com_size = dic["average community size"]
        com_size_dif = abs(com_size - clics_subgraph_size)
        if com_size_dif < closest_com_size_dif:
            closest_com_size = com_size
            closest_com_size_dif = com_size_dif
            best_t_by_com_size = threshold_list[n]
        if dic["spearman coefficient"] > highest_spearman_c:
            highest_spearman_c = dic["spearman coefficient"]
            best_t_by_spearman_c = threshold_list[n]

    return(print("\nbest threshold:\nby number of communities: " + str(best_t_by_com_num) + " with " +  str(closest_com_num) +
                 "\nby average community size: " + str(best_t_by_com_size) + " with " + str(closest_com_size) +
                 "\nby spearman coefficient: " + str(best_t_by_spearman_c) + " with " + str(highest_spearman_c)))

if __name__=="__main__":
    find_threshold(model_type, model_path, edges_path, shared_concepts_path, subgraph_path, result_path_b2, threshold)