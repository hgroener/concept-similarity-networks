import word2vecmodel
import mapping
import create_network
import create_EAT_network
import create_sense_network
import create_simlex_network
import compare_networks

from pathlib import Path
from pynorare import NoRaRe
import pandas as pd
import itertools
from tqdm import tqdm

#create file structure
Path("output/w2v").mkdir(parents=True, exist_ok=True)
Path("output/CLICS").mkdir(parents=True, exist_ok=True)
Path("output/EAT").mkdir(parents=True, exist_ok=True)
Path("output/sense").mkdir(parents=True, exist_ok=True)
Path("output/MultiSimLex").mkdir(parents=True, exist_ok=True)

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

overwrite_model = False
overwrite_w2v = False


#CLICS
compare_clics = True
clics_gml_path = 'input/CLICS/network-3-families.gml'
clics_normed = 'output/CLICS/clics_normed.gml'
clics_subgraph_path = 'output/CLICS/clics_subgraph.gml'
w_attribute_clics = "FamilyWeight"
#threshold_clics = 0.96

#EAT
compare_EAT = True
overwrite_EAT = False
norare = NoRaRe("input/NoRaRe/norare-data")
EAT = norare.datasets["Kiss-1973-EAT"]
EAT_path = 'output/EAT/EAT_graph.gml'
EAT_subgraph_path = 'output/EAT/EAT_subgraph_w2v.gml'
#threshold_EAT = 0.97

#Sense
compare_sense= True
overwrite_sense = False
sense = norare.datasets["Starostin-2000-Sense"]
sense_path = "output/sense/sense.gml"
sense_subgraph_path = "output/sense/sense_subgraph.gml"
#threshold_sense = 0.80

#MultiSimLex
SimLex_path = "output/MultiSimLex/MultiSimLex.gml"
overwrite_SimLex = True
compare_MultiSimLex = True

#evaluation
result_dics = []
b_cubed_csv_path = 'evaluation/b_cubed.csv'
pairwise_csv_path = 'evaluation/pairwise.csv'
assortativity_csv_path = 'evaluation/assortativity.csv'
adj_rand_csv_path = 'evaluation/adj_rand.csv'
result_csv_path = 'evaluation/results.csv'

models = [{"name": "w2v", "path": w2v_gml_path, "weight attribute": w_attribute, "compare": True},
          {"name": "CLICS", "path": clics_gml_path, "weight attribute": w_attribute_clics, "compare": compare_clics},
          {"name": "EAT", "path": EAT_path, "weight attribute": w_attribute, "compare": compare_EAT},
          {"name": "sense", "path": sense_path, "weight attribute": w_attribute, "compare": compare_sense},
          {"name": "MultiSimLex", "path": SimLex_path, "weight attribute": w_attribute, compare: compare_MultiSimLex}]

def get_w2v(corpus_path, model_path, vocab_path, mapped_concepts_path, edges_path, gml_path, overwrite_model = True, overwrite_gml=True):

    if overwrite_model==True or not Path(model_path).is_file():
        print("building w2v model...")
        word2vecmodel.build_model(corpus_path, model_path, vocab_path, window_size=window_size)
        mapping.get_shared_concepts(vocab_path, mapped_concepts_path)
        print("w2v model successfully built and saved to", model_path)
    else:
        print("using pre-built w2v model at", model_path)

    if overwrite_gml==True or not Path(gml_path).is_file():
        print("creating w2v network...")
        create_network.get_gml(mapped_concepts_path, model_path, edges_path, gml_path)
        print("w2v network successfully built and saved to", gml_path)
    else:
        print("using pre-built w2v network at", gml_path)

    return(print("w2v model and network ready."))


def get_prf_df(dics, key):
    prfs = [dic[key] for dic in dics]
    d = {"test set": [dic["test model"] for dic in dics], "gold set": [dic["gold model"] for dic in dics],
         "precision": [round(prf["precision"], 4) for prf in prfs], "recall": [round(prf["recall"], 4) for prf in prfs],
         "F-score": [round(prf["F-score"], 4) for prf in prfs]}
    df = pd.DataFrame(data=d)
    return(df)

def get_df(result_dics):
    test = [dic["test model"] for dic in result_dics]
    gold = [dic["gold model"] for dic in result_dics]
    b_cubed = [round(dic["B-Cubed score"]["F-score"], 4) for dic in result_dics]
    pairwise = [round(dic["pairwise evaluation score"]["F-score"], 4) for dic in result_dics]
    assortativity = [round(dic["assortativity score"], 4) for dic in result_dics]
    adj_rand = [round(dic["Adjusted Rand Coefficient"], 4) for dic in result_dics]
    spearman = [round(dic["spearman correlation"][0], 4) for dic in result_dics]
    spearman_p = [round(dic["spearman correlation"][1], 4) for dic in result_dics]
    df = pd.DataFrame({"test set": test, "gold set": gold, "B-cubed score": b_cubed, "pairwise evaluation score": pairwise, "assortativity": assortativity,
                       "adjusted rand coefficient": adj_rand, "spearman correlation": spearman, "spearman p-value": spearman_p})
    return df




if __name__=="__main__":

    #create w2v network
    get_w2v(corpus_path, model_path, vocab_path, mapped_concepts_path, edges_path, w2v_gml_path, overwrite_model=overwrite_model, overwrite_gml=overwrite_w2v)
    #create EAT network
    if not Path(EAT_path).is_file():
        create_EAT_network.build_network(EAT, EAT_path)
    else:
        if overwrite_EAT:
            create_EAT_network.build_network(EAT, EAT_path)
        else:
            print("using prebuilt EAT network at", EAT_path)

    #create Sense network
    if not Path(sense_path).is_file():
        create_sense_network.build_network(sense, sense_path)
    else:
        if overwrite_sense:
            create_sense_network.build_network(sense, sense_path)
        else:
            print("using prebuilt Sense network at", EAT_path)

    #create MultiSimLex network
    if not Path(SimLex_path).is_file():
        create_simlex_network.get_simlex_gml(SimLex_path)
    else:
        if overwrite_SimLex:
            create_simlex_network.get_simlex_gml(SimLex_path)
        else:
            print("using prebuilt MultiSimLex network at", SimLex_path)

    #compare networks to each other
    results = []
    print("comparing networks...")
    for a,b in tqdm(itertools.combinations([model for model in models if model["compare"]],2)):
        result = compare_networks.compare_networks(a["path"], b["path"], a["name"], b["name"], test_w=a["weight attribute"], gold_w=b["weight attribute"])
        results.append(result)

    #create result csvs
    df_b_cubed = get_prf_df(results, "B-Cubed score")
    df_pairwise = get_prf_df(results, "pairwise evaluation score")
    result_df = get_df(results)
    print("*** RESULTS ***\n", result_df)
    df_b_cubed.to_csv(b_cubed_csv_path, header="B-cubed scores")
    print("B-cubed scores of network comparison saved to", b_cubed_csv_path)
    df_pairwise.to_csv(pairwise_csv_path, header="pairwise evaluation scores")
    print("pairwise evaluation scores of network comparison saved to", pairwise_csv_path)
    result_df.to_csv(result_csv_path, header="network comparison")
    print("full results of network comparison saved to", result_csv_path)



