import implement_threshold
import generate_subgraph
import get_spearman
from create_network import norm_weights

import igraph
from pathlib import Path
from tqdm import tqdm

w2v_path = 'output/w2v/w2v.gml'
clics_path = 'input/CLICS/network-3-families.gml'
clics_subgraph_path = 'output/CLICS/clics_subgraph.gml'
EAT_path = 'output/EAT/EAT_graph.gml'
EAT_subgraph_path = 'output/EAT/EAT_subgraph.gml'
sense_path = 'output/sense/sense.gml'
sense_subgraph_path = 'output/sense/sense_subgraph.gml'
threshold = [n/100 for n in range(75, 100)]
n_threshold = [n/10 for n in range(10, 20)]
t_output_folder_clics = "output/w2v/t_networks_clics"
t_output_folder_EAT = "output/w2v/t_networks_EAT"
t_output_folder_sense= "output/w2v/t_networks_sense"
t = [n/100 for n in range(75, 100)]

# CLICS vs EAT
clics_eat = "output/CLICS/clics_subgraph_EAT.gml"
eat_clics = "output\EAT\EAT_subgraph_CLICS.gml"
eat_output = "output/EAT/t_networks"

def get_graph_stats(graph):
    com_num = len(graph.community_infomap())
    com_size = len(graph.vs) / com_num
    return((com_num, com_size))

def find_threshold(w2v_path, gold_path, gold_subgraph_path, threshold_list, t_output_folder):
    Path(t_output_folder).mkdir(parents=True, exist_ok=True)
    results = []
    w2v_subgraph_no_t, gold_subgraph = generate_subgraph.get_subgraphs(w2v_path, gold_path)
    gold_subgraph.write_gml(gold_subgraph_path)
    for t in tqdm(threshold_list):
        w2v_gml_path = t_output_folder + '/t' + str("{:.2f}".format(t))[2:] + ".gml"
        if not Path(w2v_gml_path).is_file():
            w2v_graph = implement_threshold.implement_threshold(w2v_subgraph_no_t, t)
            w2v_graph.write_gml(w2v_gml_path)
        w2v_graph =  igraph.read(w2v_gml_path)
        com_num, com_size = get_graph_stats(w2v_graph)
        spearman = get_spearman.get_spearman(w2v_gml_path, gold_subgraph_path)
        results.append((t, com_num, com_size, spearman[0]))

    gold_com_num, gold_com_size = get_graph_stats(gold_subgraph)

    num_difs = sorted([(result[0], abs(result[1] - gold_com_num)) for result in results], reverse = False, key=lambda tup:tup[1])
    size_difs = sorted([(result[0], abs(result[2] - gold_com_size)) for result in results], reverse = False,  key=lambda tup: tup[1])
    spearman_scores = sorted([(result[0], result[3]) for result in results], reverse = True, key=lambda tup: tup[1])

    average_ranks = []
    for t in threshold_list:
        num_difs_rank = [a for (a,b) in num_difs].index(t)
        size_difs_rank = [a for (a,b) in size_difs].index(t)
        spearman_scores_rank = [a for (a,b) in spearman_scores].index(t)
        average_rank = (num_difs_rank + size_difs_rank + spearman_scores_rank)/3
        average_ranks.append((t, average_rank))
    ranking = sorted(average_ranks, key=lambda tup:tup[1])
    print(ranking)


    return(ranking)


if __name__=="__main__":
    #ranking = find_threshold(w2v_path, clics_path, clics_subgraph_path, threshold, t_output_folder_clics)
    #ranking = find_threshold("EAT", w2v_path, EAT_path, EAT_subgraph_path, threshold, t_output_folder_EAT)
    #ranking = find_threshold(w2v_path, sense_path, sense_subgraph_path, threshold, t_output_folder_sense)
    #best_t = ranking[0][0]
    #print("Highest ranking threshold: " + str(best_t))


    clics_eat_graph = igraph.read(clics_eat)
    clics_eat_normed = norm_weights(clics_eat_graph)
    clics_eat_normed.write_gml(clics_eat)

    eat_clics_graph = igraph.read(eat_clics)
    print("CLICS", get_graph_stats(clics_eat_graph))
    print("EAT", get_graph_stats(eat_clics_graph))
    ranking = find_threshold(EAT_path, clics_path, clics_eat, n_threshold, eat_output)