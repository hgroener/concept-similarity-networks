import word2vecmodel
import mapping
import create_network
import create_EAT_network
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

#w2v
corpus_path = 'input/Brown/brown.csv'
model_path = 'output/w2v/word2vec.model'
vocab_path = 'output/w2v/model_vocab.txt'
mapped_concepts_path = 'output/w2v/mapped_concepts.tsv'
edges_path = 'output/w2v/edges.txt'
w2v_gml_path = 'output/w2v/w2v.gml'
result_path = "output/w2v/evaluation.csv"
w2v_subgraph_path_clics = 'output/w2v/w2v_subgraph_clics.gml'
w2v_subgraph_path_EAT = 'output/w2v/w2v_subgraph_EAT.gml'

overwrite_model = False
overwrite_w2v = False

result_dics = []

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


def get_w2v(corpus_path, model_path, vocab_path, mapped_concepts_path, edges_path, gml_path, overwrite_model = True, overwrite_gml=True):

    if overwrite_model==True or not Path(model_path).is_file():
        word2vecmodel.build_model(corpus_path, model_path, vocab_path)
        mapping.get_shared_concepts(vocab_path, mapped_concepts_path)

    if overwrite_gml==True or not Path(gml_path).is_file():
        create_network.get_gml(mapped_concepts_path, model_path, edges_path, gml_path)

    return(print("w2v model successfully built."))


def compare_networks(w2v_path, gold_path, w2v_subgraph_path, gold_subgraph_path, model_type, threshold, result_path):
    w2v_subgraph_raw, gold_subgraph = generate_subgraph.get_subgraphs(w2v_path, gold_path)
    w2v_subgraph = implement_threshold.implement_threshold(w2v_subgraph_raw, threshold)
    w2v_subgraph.write_gml(w2v_subgraph_path)
    gold_subgraph.write_gml(gold_subgraph_path)
    evaluation.evaluate(w2v_subgraph_path, gold_subgraph_path, model_type, threshold, result_path)
    #result_dic = evaluation.get_result_dic(w2v_subgraph_path, gold_subgraph_path, model_type, threshold)
    return(print("w2v network successfully compared to " + model_type))
    #return(result_dic)

def create_csv(result_dics, csv_path):

    b_cubed = [round(float(dic["B-Cubed score"]), 4) for dic in result_dics]
    pairwise = [round(dic["pairwise evaluation score"], 4) for dic in result_dics]
    adj_rand = [round(dic["Adjusted Rand Coefficient"], 4) for dic in result_dics]
    assortativity = [round(dic["assortativity score"], 4) for dic in result_dics]

    df = pd.DataFrame({"B-Cubed score": b_cubed, "pairwise evaluation score": pairwise, "Adjusted Rand Coefficient": adj_rand, "Assortativity": assortativity},
                      index=[dic["model type"] for dic in result_dics])

    with open(csv_path, 'a') as f:
        df.to_csv(f, header=False)

    return(print("results saved to " + csv_path))


if __name__=="__main__":

    #get w2v network
    get_w2v(corpus_path, model_path, vocab_path, mapped_concepts_path, edges_path, w2v_gml_path, overwrite_model=overwrite_model, overwrite_gml=overwrite_w2v)

    #compare to clics
    if compare_clics == True:
        compare_networks(w2v_gml_path, clics_gml_path, w2v_subgraph_path_clics, clics_subgraph_path, "CLICS", threshold_clics, result_path)
        #result_dics.append(result_dic_clics)

    #compare to EAT
    if compare_EAT == True:
        create_EAT_network.build_network(EAT, EAT_path)
        compare_networks(w2v_gml_path, EAT_path, w2v_subgraph_path_EAT, EAT_subgraph_path, "EAT", threshold_EAT, result_path)
        #result_dics.append(result_dic_EAT)

    #create result csv
    #create_csv(result_dics, result_path)

