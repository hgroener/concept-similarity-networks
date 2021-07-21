import pandas as pd
from pysem.glosses import to_concepticon
from pyconcepticon import Concepticon
import igraph

con = Concepticon()
trn_csv = "input/thematic_relatedness/trn.csv"
trn_gml = "output/thematic_relatedness/trn.gml"

def read_file(path):
    df = pd.read_csv(path)
    cue_concepts = list(set(df["CUE"]))
    responses = list(set(df["RESPONSE (R)"]))
    words = cue_concepts + responses
    return((df, words))


def map_concepts(words):
    mapped_concepts = {}
    for word in words:
        if word != "":
            try:
                mapped = to_concepticon([{'gloss': word}])
                for res in mapped[word]:
                    mapped_concepts[word] = res
            except ValueError:
                print(word + " couldn't be mapped to Concepticon")
    return mapped_concepts


def create_edges(df, mappings):
    print("creating thematic relatedness network...")
    edges = []
    no_same_mapping = []
    for i, row in df.iterrows():
        cue = row["CUE"]
        response = row["RESPONSE (R)"]
        weight = row["TOTAL No. Rs (WEIGHTED)"]
        if cue in mappings and response in mappings:
            cue_ID = mappings[cue][0]
            response_ID = mappings[response][0]
            if not cue_ID == response_ID:
                edges.append((cue_ID, response_ID, weight, (cue, response)))
            else:
                no_same_mapping.append((cue, response))
    unique_edges = {}
    nonunique = 0
    for edge in edges:
        pure_edges = [key.split(":") for key in unique_edges]
        if [edge[0], edge[1]] in pure_edges:
            concept_pair = edge[0] + ":" + edge[1]
            unique_edges[concept_pair] = ((unique_edges[concept_pair][0] + edge[2])/2, unique_edges[concept_pair][1] + [edge[3]])
            nonunique += 1
        elif [edge[1], edge[0]] in pure_edges:
            concept_pair = edge[1] + ":" + edge[0]
            unique_edges[concept_pair] = ((unique_edges[concept_pair][0] + edge[2])/2, unique_edges[concept_pair][1] + [edge[3]])
            nonunique += 1
        else:
            concept_pair = edge[0] + ":" + edge[1]
            unique_edges[concept_pair] = (edge[2], [edge[3]])
    print("number of duplicate edges:", nonunique)
    print("number of pairs mapped to the same concept:", no_same_mapping)
    return unique_edges

def create_network(mappings, edges):
    concepts = list(set([(mappings[word][0], mappings[word][1]) for word in mappings]))
    IDs = [concept[0] for concept in concepts]
    glosses = [concept[1] for concept in concepts]
    g = igraph.Graph()
    g.add_vertices(IDs)
    g.vs["ID"] = IDs
    g.vs["Gloss"] = glosses
    pure_edges = [e.split(":") for e in edges]
    weights = [edges[e][0] for e in edges]
    c_r_pairs = [edges[e][1] for e in edges]

    g.add_edges(pure_edges)
    g.es["weight"] = weights
    g.es["cue_response_pair"] = [str(l) for l in c_r_pairs]
    return(g)

def get_trn(csv, gml_path):
    df, words = read_file(csv)
    mappings = map_concepts(words)
    edges = create_edges(df, mappings)
    graph = create_network(mappings, edges)
    graph.write_gml(gml_path)
    return(print("thematic relatedness network successfully created and saved to", gml_path))


if __name__=="__main__":
    get_trn(trn_csv, trn_gml)


