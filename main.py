import word2vecmodel
import mapping
import create_network
import create_EAT_network
import create_sense_network
import create_simlex_network
import evaluation
import create_trn_network


import os
import tarfile
from pathlib import Path
from pynorare import NoRaRe
import pandas as pd
import itertools
from tqdm import tqdm
import igraph
from scipy import stats

#create file structure
Path("output/w2v").mkdir(parents=True, exist_ok=True)
Path("output/CLICS").mkdir(parents=True, exist_ok=True)
Path("output/EAT").mkdir(parents=True, exist_ok=True)
Path("output/sense").mkdir(parents=True, exist_ok=True)
Path("output/MultiSimLex").mkdir(parents=True, exist_ok=True)

#w2v w2
brown_corpus_path = 'input/Brown/brown.csv'
billion_words_zipped = "input/1b_words/1-billion-word-language-modeling-benchmark-r13output.tar.gz"
billion_words_corpus = "output/1b_words/1-billion-word-language-modeling-benchmark-r13output/training-monolingual.tokenized.shuffled"
vector_path = 'output/w2v/w2v.wordvectors'
vocab_path = 'output/w2v/w2v_vocab.txt'
mapped_concepts_path = 'output/w2v/mapped_concepts.tsv'
edges_path = 'output/w2v/edges.txt'
w2v_gml_path = 'output/w2v/w2v_no_t.gml'
window_size = 2
w_attribute = "weight"


# When overwrite-variables = True, networks and Word2Vec models are created again and overwrite existing ones.
# When overwrite variables = False, they are only created if they don't exist already
overwrite_model = False
overwrite_w2v = False
#compare variables determine if a network is included in the network comparison
compare_w2v = True

#w2v w5

vector_path_w5 = 'output/w2v/wv_w5.wordvectors'
edges_path_w5 = 'output/w2v/edges_w5.txt'
w2v_gml_path_w5 = 'output/w2v/w2v_w5_no_t.gml'
overwrite_model_w5 = False
overwrite_w2v_w5 = False
compare_w2v_w5 = True

#CLICS
compare_clics = True
clics_gml_path = 'input/CLICS/graphs/network-3-families.gml'
clics_normed = 'output/CLICS/clics_normed.gml'
clics_subgraph_path = 'output/CLICS/clics_subgraph.gml'
w_attribute_clics = "FamilyWeight"


#EAT
compare_EAT = True
overwrite_EAT = False
norare = NoRaRe("input/NoRaRe/norare-data")
EAT = norare.datasets["Kiss-1973-EAT"]
EAT_path = 'output/EAT/EAT_graph.gml'
EAT_subgraph_path = 'output/EAT/EAT_subgraph_w2v.gml'


#Sense
compare_sense= True
overwrite_sense = False
sense = norare.datasets["Starostin-2000-Sense"]
sense_path = "output/sense/sense.gml"
sense_subgraph_path = "output/sense/sense_subgraph.gml"


#MultiSimLex
SimLex_languages = ["english", "russian", "chinese", "cantonese", "arabic", "spanish", "polish", "french", "estonian", "finnish"]
SimLex_path = "output/MultiSimLex/MultiSimLex.gml"
overwrite_SimLex = False
compare_MultiSimLex = False

#MultiSimLex only utilizing english word pairs
SimLex_eng_languages = ["english"]
SimLex_eng_path = "output/MultiSimLex/MultiSimLex_eng.gml"
overwrite_SimLex_eng = False
compare_MultiSimLex_eng = False

#thematic relatedness norms
compare_trn= False
overwrite_trn = False
trn_xlsx = "input/thematic_relatedness/13428_2015_679_MOESM2_ESM.xlsx"
trn_csv = "input/thematic_relatedness/trn.csv"
trn_gml = "output/thematic_relatedness/trn.gml"
trn_eval_csv = "evalution/trn_eval.csv"

#evaluation
result_dics = []
b_cubed_csv_path = 'evaluation/b_cubed.csv'
pairwise_csv_path = 'evaluation/pairwise.csv'
assortativity_csv_path = 'evaluation/assortativity.csv'
adj_rand_csv_path = 'evaluation/adj_rand.csv'
result_csv_path = 'evaluation/results.csv'
SimLex_csv_path = 'evaluation/SimLex_results.csv'
trn_eval_csv = 'evaluation/trn_eval.csv'
top_10_path = 'evaluation/top_10s.csv'
rank_dif_path = 'evaluation/rank_difs.csv'
calculate_p_values = False

#evaluation of metrics
metrics_eval_path = 'evaluation/metrics.csv'

#dictionary containing information about each of the networks, that can be iterated through to save effort
models = [{"name": "CBOW w2", "path": w2v_gml_path, "weight attribute": w_attribute, "compare": compare_w2v, "type": "w2v"},
          {"name": "CBOW w5", "path": w2v_gml_path_w5, "weight attribute": w_attribute, "compare": compare_w2v_w5, "type": "w2v"},
          {"name": "CLICS", "path": clics_gml_path, "weight attribute": w_attribute_clics, "compare": compare_clics, "type": "CLICS"},
          {"name": "EAT", "path": EAT_path, "weight attribute": w_attribute, "compare": compare_EAT, "type": "EAT"},
          {"name": "SENSE", "path": sense_path, "weight attribute": w_attribute, "compare": compare_sense, "type": "sense"},
          {"name": "MultiSimLex", "path": SimLex_path, "weight attribute": w_attribute, "compare": compare_MultiSimLex, "type": "MultiSimLex"},
          {"name": "MultiSimLex English", "path": SimLex_eng_path, "weight attribute": w_attribute, "compare": compare_MultiSimLex_eng, "type": "MultiSimLex"},
          {"name": "Thematic Relatedness Norms", "path": trn_gml, "weight attribute": w_attribute, "compare": compare_trn, "type": "thematic relatedness norms"}
          ]

metrics = ["B-cubed score", "pairwise evaluation score", "assortativity", "adjusted rand coefficient", "spearman correlation"]

# create w2v models
def get_w2v(brown_corpus, google_corpus, vector_path, vocab_path, mapped_concepts_path, edges_path, gml_path, window_size = 2, google_vectors=False, overwrite_model = True, overwrite_gml=True):

    if overwrite_model==True or not Path(vector_path).is_file():
        print("building w2v model...")
        word2vecmodel.build_model(brown_corpus, google_corpus, vector_path, vocab_path, window_size=window_size)
        mapping.get_shared_concepts(vocab_path, mapped_concepts_path)
        print("w2v model successfully built, vectors saved to", vector_path)
    else:
        print("using pre-trained w2v vectors at", vector_path)

    if overwrite_gml==True or not Path(gml_path).is_file():
        print("creating w2v network...")
        create_network.get_gml(mapped_concepts_path, vector_path, edges_path, gml_path, threshold=False)
        print("w2v network successfully built and saved to", gml_path)
    else:
        print("using pre-built w2v network at", gml_path)

    return(print("w2v model and network ready."))


#create pandas-dataframes for results
def get_prf_df(dics, key):
    prfs = [dic[key] for dic in dics]
    d = {"graph 1": [dic["model 1"] for dic in dics], "graph 2": [dic["model 2"] for dic in dics],
         "precision": [round(prf["precision"], 4) for prf in prfs], "recall": [round(prf["recall"], 4) for prf in prfs],
         "F-score": [round(prf["F-score"], 4) for prf in prfs]}
    df = pd.DataFrame(data=d)
    return(df)

def get_df(result_dics):
    test = [dic["model 1"] for dic in result_dics]
    gold = [dic["model 2"] for dic in result_dics]
    nodes = [dic["nodes"] for dic in result_dics]
    edges = [dic["edges"] for dic in result_dics]
    b_cubed = [round(dic["B-Cubed score"], 4) for dic in result_dics]
    pairwise = [round(dic["pairwise evaluation score"], 4) for dic in result_dics]
    assortativity = [round(dic["assortativity score"], 4) for dic in result_dics]
    adj_rand = [round(dic["Adjusted Rand Coefficient"], 4) for dic in result_dics]
    spearman = [round(dic["spearman correlation"][0], 4) for dic in result_dics]
    spearman_p = [round(dic["spearman correlation"][1], 4) for dic in result_dics]
    df = pd.DataFrame({"test set": test, "gold set": gold, "nodes compared": nodes, "edges compared": edges, "B-cubed score": b_cubed,
                       "pairwise evaluation score": pairwise, "assortativity": assortativity,
                       "adjusted rand coefficient": adj_rand, "spearman correlation": spearman, "spearman p-value": spearman_p})
    return df

def get_p_df(results):
    test = [dic["model 1"] for dic in results]
    gold = [dic["model 2"] for dic in results]
    nodes = [dic["nodes"] for dic in results]
    edges = [dic["edges"] for dic in results]

    b_cubed = [round(dic["B-Cubed score"][0], 4) for dic in results]
    p_b_cubed = [round(dic["B-Cubed score"][1], 4) for dic in results]

    pairwise = [round(dic["pairwise evaluation score"][0], 4) for dic in results]
    p_pairwise = [round(dic["pairwise evaluation score"][1], 4) for dic in results]

    assortativity = [round(dic["assortativity score"][0], 4) for dic in results]
    p_assortativity = [round(dic["assortativity score"][1], 4) for dic in results]

    adj_rand = [round(dic["Adjusted Rand Coefficient"][0], 4) for dic in results]
    p_adj_rand = [round(dic["Adjusted Rand Coefficient"][1], 4) for dic in results]

    spearman = [round(dic["spearman correlation"][0], 4) for dic in results]
    p_spearman = [round(dic["spearman correlation"][1], 4) for dic in results]

    df = pd.DataFrame(
        {"test set": test, "gold set": gold, "nodes compared": nodes, "edges compared": edges, "B-cubed score": b_cubed, "B-cubed p-value": p_b_cubed,
         "pairwise evaluation score": pairwise, "pairwise evaluation p value": p_pairwise,  "assortativity": assortativity, "assortativity p-value": p_assortativity,
         "adjusted rand coefficient": adj_rand, "adjusted rand p-value": p_adj_rand, "spearman correlation": spearman, "spearman p-value": p_spearman})
    return df


#calculates correlation between metrics
def metrics_correlation(df, metrics, path):
    print("comparing metrics...")
    combs = list(itertools.combinations(metrics, 2))
    print("combs:", combs)
    test_metrics = [m[0] for m in combs]
    print("test metric:", test_metrics)
    print("length test metrics:", len(test_metrics))
    gold_metrics = [m[1] for m in combs]
    print("gold metric:", gold_metrics)
    print("length gold metric:", len(gold_metrics))
    spearman = [stats.spearmanr(df[m1].tolist(),df[m2].tolist()) for (m1,m2) in combs]
    r = [s[0] for s in spearman]
    p = [s[1] for s in spearman]
    print("r:", r)
    print("length r:", len(r))
    print("p:", p)
    print("length p:", len(p))
    df = pd.DataFrame({"metric 1": test_metrics, "metric 2": gold_metrics, "spearman ranked coefficient": r, "spearman p-value": p})
    df.to_csv(path)

    return(print("evaluation of metrics done and saved to", path))

# outputs the 10 highest-weight edges in each network
def get_highest_weight(models, path):
    top10s = {}
    for model in models:
        if model["compare"] == True:
            graph = igraph.read(model["path"])
            edgelist = graph.get_edgelist()
            weights = graph.es[model["weight attribute"]]

            edge_IDs = {graph.vs[id1]["Gloss"] + " : " + graph.vs[id2]["Gloss"]: weights[i] for i, (id1, id2) in enumerate(edgelist)}
            pairs = list(edge_IDs.keys())
            pairs.sort(key=lambda x: edge_IDs[x], reverse=True)
            top_10 = pairs[:10]

            top10s[model["name"]] = top_10

    df = pd.DataFrame(top10s)
    df.to_csv(path, index=False)
    return(print("highest rated pairs in all networks saved to", path))

def get_rank_dif_df(results, output):
    d = {dic["model 1"] + " : "  + dic["model 2"]: dic["most differently rated pairs"] for dic in results}
    df = pd.DataFrame(d)
    df.to_csv(output, index=False)
    return("most dissimilar edges saved to", output )


if __name__=="__main__":

    #unzip 1 billion word corpus
    if not os.path.isfile(billion_words_corpus):
        tar = tarfile.open(billion_words_zipped, "r:gz")
        tar.extractall(path="output/1b_words")

    #convert thematic relatedness norms file to .csv-format
    if not os.path.isfile(trn_csv):
        trn_data = pd.read_excel(trn_xlsx, index_col=None)
        trn_data.to_csv(trn_csv, encoding='utf-8')
        print("trn data successfully converted to .csv-file")


    #create w2v network w2
    get_w2v(brown_corpus_path,billion_words_corpus, vector_path, vocab_path, mapped_concepts_path, edges_path,
            w2v_gml_path, window_size = 2, overwrite_model=overwrite_model, overwrite_gml=overwrite_w2v)
    #create w2v network w5
    get_w2v(brown_corpus_path,billion_words_corpus, vector_path_w5, vocab_path, mapped_concepts_path, edges_path_w5,
            w2v_gml_path_w5, window_size = 5, overwrite_model=overwrite_model_w5, overwrite_gml=overwrite_w2v_w5)

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
        create_simlex_network.get_simlex_gml(SimLex_languages, SimLex_path)
    else:
        if overwrite_SimLex:
            create_simlex_network.get_simlex_gml(SimLex_languages, SimLex_path)
        else:
            print("using prebuilt MultiSimLex network at", SimLex_path)
    SimLex_edges = create_simlex_network.create_simlex_network(SimLex_languages, return_graph=False)
    #create MultiSimLex English network
    if not Path(SimLex_eng_path).is_file():
        create_simlex_network.get_simlex_gml(SimLex_eng_languages, SimLex_eng_path)
    else:
        if overwrite_SimLex_eng:
            create_simlex_network.get_simlex_gml(SimLex_eng_languages, SimLex_eng_path)
        else:
            print("using prebuilt MultiSimLex-eng network at", SimLex_eng_path)

    #create thematic relatedness norms network
    if not Path(trn_gml).is_file():
        create_trn_network.get_trn(trn_csv, trn_gml)
    else:
        if overwrite_trn:
            create_trn_network.get_trn(trn_csv, trn_gml)
        else:
            print("using prebuilt thematic relatedness network at", trn_gml)

    #compare networks
    if calculate_p_values:
        results = evaluation.get_results_p(models, p_values=True, get_rank_difs=True)
        result_df = get_p_df(results)
    else:
        results = evaluation.get_results_p(models, p_values=False, get_rank_difs=True)
        result_df = get_df(results)


    #create result csvs
    df_b_cubed = get_prf_df(results, "B-cubed metrics")
    df_pairwise = get_prf_df(results, "pairwise evaluation metrics")
    print("*** RESULTS ***\n", result_df)
    df_b_cubed.to_csv(b_cubed_csv_path, header="B-cubed scores")
    print("B-cubed scores of network comparison saved to", b_cubed_csv_path)
    df_pairwise.to_csv(pairwise_csv_path, header="pairwise evaluation scores")
    print("pairwise evaluation scores of network comparison saved to", pairwise_csv_path)
    result_df.to_csv(result_csv_path, header="network comparison")
    print("full results of network comparison saved to", result_csv_path)


    # evalate networks with MultiSimLex and thematic relatedness norms
    evaluation.eval_network(models, SimLex_path, trn_gml, SimLex_csv_path, trn_eval_csv)


    # get 10 most similar pairs for each network
    get_highest_weight(models, top_10_path)

    # get 5 most differently ranked edges for each pair of networks
    get_rank_dif_df(results, rank_dif_path)
