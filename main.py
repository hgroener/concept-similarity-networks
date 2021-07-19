import word2vecmodel
import mapping
import create_network
import create_EAT_network
import create_sense_network
import create_simlex_network
import evaluation
import create_trn_network
import get_spearman

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
google_corpus_path = 'output/GoogleNews/1-billion-word-language-modeling-benchmark-r13output/training-monolingual.tokenized.shuffled'
vector_path = 'output/w2v/w2v.wordvectors'
#model_path = 'output/w2v/word2vec.model'
vocab_path = 'output/w2v/w2v_vocab.txt'
mapped_concepts_path = 'output/w2v/mapped_concepts.tsv'
edges_path = 'output/w2v/edges.txt'
w2v_gml_path = 'output/w2v/w2v_no_t.gml'
window_size = 2
w_attribute = "weight"

overwrite_model = False
overwrite_w2v = False
compare_w2v = True

#w2v w5

vector_path_w5 = 'output/w2v/wv_w5.wordvectors'
#model_path_w5 = 'output/w2v/word2vec_w5.model'
edges_path_w5 = 'output/w2v/edges_w5.txt'
#w2v_gml_path_w5 = 'output/w2v/w2v_w5.gml'
w2v_gml_path_w5 = 'output/w2v/w2v_w5_no_t.gml'
overwrite_model_w5 = False
overwrite_w2v_w5 = False
compare_w2v_w5 = True

#google vectors
google_path = "input\google_pretrained_w2v\word2vec-google-news-300.gz"
google_vectors = 'output/w2v/google.wordvectors'
google_vocab = 'output/w2v/google/google_vocab.txt'
google_mapped_concepts_path = 'output/w2v/google/google_mapped_concepts.tsv'
google_edges_path = 'output/w2v/google/google_edges.txt'
google_gml_path = 'output/w2v/google/google.gml'
compare_google = False
overwrite_google = False
overwrite_google_gml = False


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

#evaluation of metrics
metrics_eval_path = 'evaluation/metrics.csv'

models = [{"name": "w2v w2", "path": w2v_gml_path, "weight attribute": w_attribute, "compare": compare_w2v, "type": "w2v"},
          {"name": "w2v w5", "path": w2v_gml_path_w5, "weight attribute": w_attribute, "compare": compare_w2v_w5, "type": "w2v"},
          {"name": "w2v Google", "path": google_gml_path, "weight attribute": w_attribute, "compare": compare_google, "type": "w2v"},
          {"name": "CLICS", "path": clics_gml_path, "weight attribute": w_attribute_clics, "compare": compare_clics, "type": "CLICS"},
          {"name": "EAT", "path": EAT_path, "weight attribute": w_attribute, "compare": compare_EAT, "type": "EAT"},
          {"name": "sense", "path": sense_path, "weight attribute": w_attribute, "compare": compare_sense, "type": "sense"},
          {"name": "MultiSimLex", "path": SimLex_path, "weight attribute": w_attribute, "compare": compare_MultiSimLex, "type": "MultiSimLex"},
          {"name": "MultiSimLex English", "path": SimLex_eng_path, "weight attribute": w_attribute, "compare": compare_MultiSimLex_eng, "type": "MultiSimLex"},
          {"name": "thematic relatedness norms", "path": trn_gml, "weight attribute": w_attribute, "compare": compare_trn, "type": "thematic relatedness norms"}
          ]

metrics = ["B-cubed score", "pairwise evaluation score", "assortativity", "adjusted rand coefficient", "spearman correlation"]


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
    nodes = [dic["nodes"] for dic in result_dics]
    edges = [dic["edges"] for dic in result_dics]
    b_cubed = [round(dic["B-Cubed score"]["F-score"], 4) for dic in result_dics]
    pairwise = [round(dic["pairwise evaluation score"]["F-score"], 4) for dic in result_dics]
    assortativity = [round(dic["assortativity score"], 4) for dic in result_dics]
    adj_rand = [round(dic["Adjusted Rand Coefficient"], 4) for dic in result_dics]
    spearman = [round(dic["spearman correlation"][0], 4) for dic in result_dics]
    spearman_p = [round(dic["spearman correlation"][1], 4) for dic in result_dics]
    df = pd.DataFrame({"test set": test, "gold set": gold, "nodes compared": nodes, "edges compared": edges, "B-cubed score": b_cubed,
                       "pairwise evaluation score": pairwise, "assortativity": assortativity,
                       "adjusted rand coefficient": adj_rand, "spearman correlation": spearman, "spearman p-value": spearman_p})
    return df

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


def get_highest_weight(models, path):
    top10s = {}
    for model in models:
        graph = igraph.read(model["path"])
        edgelist = graph.get_edgelist()
        weights = graph.es[model["weight attribute"]]

        edge_IDs = {graph.vs[id1]["Gloss"] + " : " + graph.vs[id2]["Gloss"]: weights[i] for i, (id1, id2) in enumerate(edgelist)}
        pairs = list(edge_IDs.keys())
        pairs.sort(key=lambda x: edge_IDs[x], reverse=True)
        top_10 = pairs[:10]
        top_10_weights = []
        for pair in top_10:
            w  = edge_IDs[pair]
            top_10_weights.append(pair + ": " + str(w))

        top10s[model["name"]] = top_10_weights
        #print("10 highest ranking pairs:")
        #top_10_str = "#\tpair\tscore\n"
        #for i, pair in enumerate(top_10):
         #   top_10_str += str(i+1) + "\t" + pair + ":\t" +  str(edge_IDs[pair]) + "\n"
        #print(top_10_str)
    df = pd.DataFrame(top10s)
    df.to_csv(path)
    return(top10s)

def get_rank_dif_df(rank_difs, output):
    df = pd.DataFrame(rank_difs)
    df.to_csv(output)
    return("most dissimilar edges saved to", output )







if __name__=="__main__":

    #create w2v network w2
    get_w2v(brown_corpus_path,google_corpus_path, vector_path, vocab_path, mapped_concepts_path, edges_path, w2v_gml_path, window_size = 2, overwrite_model=overwrite_model, overwrite_gml=overwrite_w2v)
    #create w2v network w5
    get_w2v(brown_corpus_path,google_corpus_path, vector_path_w5, vocab_path, mapped_concepts_path, edges_path_w5, w2v_gml_path_w5, window_size = 5, overwrite_model=overwrite_model_w5, overwrite_gml=overwrite_w2v_w5)
    #create google w2v network
    #get_w2v(google_path, google_vectors, google_vocab, google_mapped_concepts_path, google_edges_path, google_gml_path, overwrite_model= overwrite_google, overwrite_gml = overwrite_google_gml, google_vectors=True)
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
    results = []
    highest_rank_difs = []
    print("comparing networks...")
    for a,b in tqdm(itertools.combinations([model for model in models if model["compare"]],2)):
        if not a["type"] == b["type"]:
            print("comparing network {0} to network {1}".format(a["name"], b["name"]))
            graph_a = igraph.read(a["path"])
            graph_b = igraph.read(b["path"])
            result = evaluation.get_result_dic(graph_a, graph_b, a["name"], b["name"], test_w=a["weight attribute"], gold_w=b["weight attribute"], nodes = True, edges = True)
            results.append(result)
            rank_dif = evaluation.highest_rank_difference(graph_a, graph_b, w1=a["weight attribute"], w2=b["weight attribute"])
            highest_rank_difs.append(rank_dif)
            print("successfully compared network {0} to network {1}".format(a["name"], b["name"]))

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


    # evalate networks with MultiSimLex and thematic relatedness norms
    evaluation.eval_network(models, SimLex_path, trn_gml, SimLex_csv_path, trn_eval_csv)

    # evaluate metrics
    #metrics_correlation(result_df, metrics, metrics_eval_path)

    # get 10 most similar pairs for each network
    print(get_highest_weight([model for model in models if model["compare"]], top_10_path))


    get_rank_dif_df(highest_rank_difs, rank_dif_path)