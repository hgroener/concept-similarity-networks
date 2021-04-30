import word2vecmodel
import mapping
import create_network
import create_EAT_network
import create_sense_network
import generate_subgraph
import implement_threshold
import evaluation

from pathlib import Path
from pynorare import NoRaRe
import pandas as pd

#create file structure
Path("output/w2v").mkdir(parents=True, exist_ok=True)
Path("output/CLICS").mkdir(parents=True, exist_ok=True)
Path("output/EAT").mkdir(parents=True, exist_ok=True)
Path("output/sense").mkdir(parents=True, exist_ok=True)
Path("evaluation").mkdir(parents=True, exist_ok=True)

#w2v
corpus_path = 'input/Brown/brown.csv'
model_path = 'output/w2v/word2vec.model'
vocab_path = 'output/w2v/model_vocab.txt'
mapped_concepts_path = 'output/w2v/mapped_concepts.tsv'
edges_path = 'output/w2v/edges.txt'
w2v_gml_path = 'output/w2v/w2v.gml'
result_path = "output/w2v/evaluation.txt"
w2v_subgraph_path_clics = 'output/w2v/w2v_subgraph_clics.gml'
w2v_subgraph_path_EAT = 'output/w2v/w2v_subgraph_EAT.gml'
w2v_subgraph_path_sense = 'output/w2v/w2v_subgraph_sense.gml'
window_size = 3

overwrite_model = True
overwrite_w2v = True


#CLICS
compare_clics = True
clics_gml_path = 'input/CLICS/network-3-families.gml'
clics_subgraph_path = 'output/CLICS/clics_subgraph.gml'
threshold_clics = 0.96

#EAT
compare_EAT = True
norare = NoRaRe("input/NoRaRe/norare-data")
EAT = norare.datasets["Kiss-1973-EAT"]
EAT_path = 'output/EAT/EAT_graph.gml'
EAT_subgraph_path = 'output/EAT/EAT_subgraph_w2v.gml'
threshold_EAT = 0.97

#Sense
compare_sense=True
sense = norare.datasets["Starostin-2000-Sense"]
sense_path = "output/sense/sense.gml"
sense_subgraph_path = "output/sense/sense_subgraph.gml"
threshold_sense = 0.93

#evaluation
result_dics = []
b_cubed_csv_path = 'evaluation/b_cubed.csv'
pairwise_csv_path = 'evaluation/pairwise.csv'
assortativity_csv_path = 'evaluation/assortativity.csv'
adj_rand_csv_path = 'evaluation/adj_rand.csv'

def get_w2v(corpus_path, model_path, vocab_path, mapped_concepts_path, edges_path, gml_path, overwrite_model = True, overwrite_gml=True):

    if overwrite_model==True or not Path(model_path).is_file():
        word2vecmodel.build_model(corpus_path, model_path, vocab_path, window_size=window_size)
        mapping.get_shared_concepts(vocab_path, mapped_concepts_path)

    if overwrite_gml==True or not Path(gml_path).is_file():
        create_network.get_gml(mapped_concepts_path, model_path, edges_path, gml_path)

    return(print("w2v model successfully built."))


def compare_networks(w2v_path, gold_path, w2v_subgraph_path, gold_subgraph_path, model_type, threshold, result_path):
    w2v_subgraph_raw, gold_subgraph = generate_subgraph.get_subgraphs(w2v_path, gold_path)
    w2v_subgraph = implement_threshold.implement_threshold(w2v_subgraph_raw, threshold)
    w2v_subgraph.write_gml(w2v_subgraph_path)
    gold_subgraph.write_gml(gold_subgraph_path)
    #evaluation.evaluate(w2v_subgraph_path, gold_subgraph_path, model_type, threshold, result_path)
    result_dic = evaluation.get_result_dic(w2v_subgraph_path, gold_subgraph_path, model_type, threshold)
    #return(print("w2v network successfully compared to " + model_type))
    return(result_dic)

def get_prf_df(dics, key):
    prfs = [dic[key] for dic in dics]
    d = {"dataset": [dic["model type"] for dic in dics], "precision": [round(prf["precision"], 4) for prf in prfs], "recall": [round(prf["recall"], 4) for prf in prfs],
         "F-score": [round(prf["F-score"], 4) for prf in prfs]}
    df = pd.DataFrame(data=d)
    return(df)


def create_csv(result_dics, b_cubed_path, pairwise_path, assortativity_path, adj_rand_path):
    df_b_cubed = get_prf_df(result_dics, "B-Cubed score")
    df_pairwise = get_prf_df(result_dics, "pairwise evaluation score")
    df_assortativity = pd.DataFrame(data={"dataset": [dic["model type"] for dic in result_dics],
                                          "assortativity": [round(dic["assortativity score"], 4) for dic in
                                                            result_dics]})
    df_adj_rand = pd.DataFrame(data={"dataset": [dic["model type"] for dic in result_dics],
                                     "adjusted rand coefficient": [round(dic["Adjusted Rand Coefficient"], 4) for dic in
                                                                   result_dics]})

    df_b_cubed.to_csv(b_cubed_path, header="B-Cubed")
    df_pairwise.to_csv(pairwise_path, header="pairwise evaluation")
    df_assortativity.to_csv(assortativity_path, header="assortativity")
    df_adj_rand.to_csv(adj_rand_path, header="adjusted rand coefficient")

    return (print("results saved"))


if __name__=="__main__":

    #get w2v network
    get_w2v(corpus_path, model_path, vocab_path, mapped_concepts_path, edges_path, w2v_gml_path, overwrite_model=overwrite_model, overwrite_gml=overwrite_w2v)

    #compare to clics
    if compare_clics == True:
        result_dic_clics = compare_networks(w2v_gml_path, clics_gml_path, w2v_subgraph_path_clics, clics_subgraph_path, "CLICS", threshold_clics, result_path)
        result_dics.append(result_dic_clics)

    #compare to EAT
    if compare_EAT == True:
        create_EAT_network.build_network(EAT, EAT_path)
        result_dic_EAT = compare_networks(w2v_gml_path, EAT_path, w2v_subgraph_path_EAT, EAT_subgraph_path, "EAT", threshold_EAT, result_path)
        result_dics.append(result_dic_EAT)

    #compare to sense
    if compare_sense == True:
        create_sense_network.build_network(sense, sense_path)
        result_dic_sense = compare_networks(w2v_gml_path, sense_path, w2v_subgraph_path_sense, sense_subgraph_path, "Sense", threshold_sense, result_path)
        result_dics.append(result_dic_sense)

    #create result csvs
    create_csv(result_dics, b_cubed_csv_path, pairwise_csv_path, assortativity_csv_path, adj_rand_csv_path)



