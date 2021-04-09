import evaluation
import implement_threshold
import generate_subgraph

from pathlib import Path
from tqdm import tqdm

w2v_path = 'output/w2v/w2v.gml'
clics_path = 'input/CLICS/network-3-families.gml'
clics_subgraph_path = 'output/CLICS/clics_subgraph.gml'
EAT_path = 'output/EAT/EAT_graph.gml'
EAT_subgraph_path = 'output/EAT/EAT_subgraph.gml'
sense_path = 'output/sense/sense.gml'
sense_subgraph_path = 'output/sense/sense_subgraph.gml'
threshold = [0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99]
t_output_folder_clics = "output/w2v/t_networks_clics"
t_output_folder_EAT = "output/w2v/t_networks_EAT"
t_output_folder_sense= "output/w2v/t_networks_sense"

def get_graph_stats(graph):
    com_num = len(graph.community_infomap())
    com_size = len(graph.vs) / com_num
    return((com_num, com_size))

def find_threshold(model_type, w2v_path, comparison_graph_path, comparison_subgraph_path, threshold_list, t_output_folder):
    Path(t_output_folder).mkdir(parents=True, exist_ok=True)
    results = []
    w2v_subgraph_no_t, comparison_subgraph = generate_subgraph.get_subgraphs(w2v_path, comparison_graph_path)
    comparison_subgraph.write_gml(comparison_subgraph_path)
    for t in tqdm(threshold_list):
        w2v_gml_path = t_output_folder + '/w2v_t' + str("{:.2f}".format(t))[2:] + ".gml"
        if not Path(w2v_gml_path).is_file():
            w2v_graph = implement_threshold.implement_threshold(w2v_subgraph_no_t, t)
            w2v_graph.write_gml(w2v_gml_path)
        result_dic = evaluation.get_result_dic(w2v_gml_path, comparison_subgraph_path, model_type, t, b_cubed = False, pe = False, adj_rand = False, assortativity = False)
        results.append(result_dic)

    comparison_com_num, comparison_com_size = get_graph_stats(comparison_subgraph)

    num_difs = sorted([(dic["threshold"], dic["number of communities"] - comparison_com_num) for dic in results], reverse = True, key=lambda tup:tup[1])
    size_difs = sorted([(dic["threshold"], dic["average community size"] - comparison_com_size) for dic in results], reverse = True,  key=lambda tup: tup[1])
    spearman_scores = sorted([(dic["threshold"], dic["spearman coefficient"]["spearman correlation"]) for dic in results], reverse = True, key=lambda tup: tup[1])
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
    #ranking = find_threshold("CLICS", w2v_path, clics_path, clics_subgraph_path, threshold, t_output_folder_clics)
    #ranking = find_threshold("EAT", w2v_path, EAT_path, EAT_subgraph_path, threshold, t_output_folder_EAT)
    ranking = find_threshold("Sense", w2v_path, sense_path, sense_subgraph_path, threshold, t_output_folder_sense)
    best_t = ranking[0][0]
    print("Highest ranking threshold: " + str(best_t))