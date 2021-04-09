import igraph
from pynorare import NoRaRe
import itertools

norare = NoRaRe("input/NoRaRe/norare-data")
sense = norare.datasets["Starostin-2000-Sense"]
output_file = 'output/sense/sense.gml'


def convert_sense(sense):
    cids = []
    concept_list = []
    gloss_dict = {}
    for cid, concept in sense.concepts.items():
        concept_list.append(concept)
        cids.append(str(cid))

    edges = []
    for concept, other_concept in itertools.combinations(concept_list,2):
        sense_intersection = [sense for sense in concept["senses"].split(";") if sense in other_concept["senses"].split(";")]
        intersection_len = len(sense_intersection)
        if intersection_len > 0:
            edges.append((str(concept["concepticon_id"]), str(other_concept["concepticon_id"]), intersection_len))


    return((cids, edges))

def build_network(sense, output_file):
    cids, edges = convert_sense(sense)
    EAT_graph = igraph.Graph()
    EAT_graph.add_vertices(cids)
    EAT_graph.vs["ID"] = cids
    EAT_graph.add_edges([(ID, other_ID) for (ID, other_ID, weight) in edges])
    EAT_graph.es['weight'] = [weight for ID, other_ID, weight in edges]
    EAT_graph.write_gml(output_file)
    return(print("sense network successfully built and saved to " + output_file))

if __name__=="__main__":
    build_network(sense, output_file)
