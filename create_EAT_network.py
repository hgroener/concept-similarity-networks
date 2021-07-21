from pynorare import NoRaRe
from tqdm import tqdm
from pysem.glosses import to_concepticon
import igraph
import re

norare = NoRaRe("input/NoRaRe/norare-data")
EAT = norare.datasets["Kiss-1973-EAT"]
output_file = 'output/EAT/EAT_graph.gml'

#collects IDs and glosses of concepts words in the EAT were mapped to, maps unmapped words, returns tuples representing edges
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

#builds igraph network, saves to .gml-file
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



if __name__=="__main__":
    build_network(EAT, output_file)

