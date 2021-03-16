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

def find_threshold(model_type, model_path, edges_path, shared_concepts_path, CLICS_subgraph_path, result_path_b2,
                   threshold_list):
    Path("output/w2v_networks").mkdir(parents=True, exist_ok=True)
    results = []
    for t in tqdm(threshold_list):
        w2v_gml_path = 'output/w2v_networks/w2v_t' + str("{:.2f}".format(t))[2:] + ".gml"
        w2v_gml_file_path = Path(w2v_gml_path)
        if not w2v_gml_file_path.is_file():
            create_network.get_gml(shared_concepts_path, model_path, edges_path, t, w2v_gml_path)
        result_dic = get_b_cubed.get_b_cubed(w2v_gml_path, CLICS_subgraph_path, model_type, result_path_b2, t,
                                             return_scores=True)
        result_dic["threshold"] = t
        results.append(result_dic)

    num_difs = sorted([(dic["threshold"], dic["communities"] - clics_subgraph_num) for dic in results], reverse = True, key=lambda tup:tup[1])
    size_difs = sorted([(dic["threshold"], dic["average community size"] - clics_subgraph_size) for dic in results], reverse = True,  key=lambda tup: tup[1])
    spearman_scores = sorted([(dic["threshold"], dic["spearman coefficient"]) for dic in results], reverse = True, key=lambda tup: tup[1])
    average_ranks = []
    for t in threshold_list:
        num_difs_rank = [a for (a,b) in num_difs].index(t)
        size_difs_rank = [a for (a,b) in size_difs].index(t)
        spearman_scores_rank = [a for (a,b) in spearman_scores].index(t)
        average_rank = (num_difs_rank + size_difs_rank + spearman_scores_rank)/3
        average_ranks.append((t, average_rank))
    ranking = sorted(average_ranks, key=lambda tup:tup[1])


    return(ranking)

if __name__=="__main__":
    ranking = find_threshold(model_type, model_path, edges_path, shared_concepts_path, subgraph_path, result_path_b2, threshold)
    best_t = ranking[0][0]
    print("Highest ranking threshold: " + str(best_t))