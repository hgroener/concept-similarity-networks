from pynorare import NoRaRe
from tqdm import tqdm
from pysen.glosses import to_concepticon
import igraph
import re
import itertools

norare = NoRaRe("input/NoRaRe/norare-data")
EAT = norare.datasets["Kiss-1973-EAT"]
output_file = 'output/EAT/EAT_graph.gml'

def convert_EAT(EAT):
    cids = []
    concept_list = []
    gloss_dict = {}
    for cid, concept in tqdm(EAT.concepts.items()):
        concept_list.append(concept)
        cids.append(str(cid))
        gloss_dict[concept["concepticon_gloss"]] = cid


    edges = []
    failed_mappings = []
    for concept in concept_list:
        edge_list = concept["edges"]
        for edge in edge_list:
            if re.search(".*:\d+", edge):
                gloss, weight = edge.split(":")
                if gloss in gloss_dict.keys():
                    linked_ID = str(gloss_dict[gloss])
                    edges.append((str(concept["concepticon_id"]), linked_ID, int(weight)))
                else:
                    #empty strings cause error if not intercepted
                    try:
                        mapped = to_concepticon([{'gloss': gloss}])
                    except ValueError:
                        mapped = {}
                        failed_mappings.append(edge)
                    #once again, empty strings cause KeyErrors
                    if gloss in mapped:
                        for res in mapped[gloss]:
                            linked_ID = res[0]
                            if not linked_ID in cids:
                                cids.append(linked_ID)
                            edges.append((str(concept["concepticon_id"]), linked_ID, int(weight)))
    glosses = list(gloss_dict.keys())
    print("edges that couldn't be mapped:", failed_mappings)
    return((cids, glosses, edges))

def build_network(EAT, output_file):
    cids, glosses, edges = convert_EAT(EAT)
    EAT_graph = igraph.Graph()
    EAT_graph.add_vertices(cids)
    EAT_graph.vs["ID"] = cids
    EAT_graph.vs["Gloss"] = glosses
    EAT_graph.add_edges([(ID, other_ID) for (ID, other_ID, weight) in edges])
    EAT_graph.es['weight'] = [weight for ID, other_ID, weight in edges]
    EAT_graph.write_gml(output_file)
    return(print("EAT network successfully built and saved to " + output_file))

def get_density(graph):
    possible_edge_len = len(list(itertools.combinations(graph.vs, 2)))
    edge_len = len(graph.es)
    density = edge_len/possible_edge_len
    return(density)

if __name__=="__main__":
    build_network(EAT, output_file)
    EAT_graph = igraph.read(output_file)
    print("network density: ", get_density(EAT_graph))
