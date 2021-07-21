import igraph
from pynorare import NoRaRe
import itertools
from tqdm import tqdm

# creates SENSE network from NoRaRe data
norare = NoRaRe("input/NoRaRe/norare-data")
sense = norare.datasets["Starostin-2000-Sense"]
output_file = 'output/sense/sense.gml'


# reads concepts mapped to SENSE from NoRaRe, creates edges based on the intersection of semantic constituents between concepts
#outputs Concepticon IDs, Glosses and edges, which are a list of tuples containing the IDs of the concepts that are connected and the weight of the edge
def convert_sense(sense):
    cids = []
    concept_list = []
    glosses = []
    print("collecting concepts...")
    for cid, concept in tqdm(sense.concepts.items()):
        concept_list.append(concept)
        glosses.append(concept["concepticon_gloss"])
        cids.append(str(cid))

    edges = []
    print("creating edges...")
    for concept, other_concept in tqdm(itertools.combinations(concept_list,2)):
        sense_intersection = [sense for sense in concept["senses"].split(";") if sense in other_concept["senses"].split(";")]

        intersection_len = len(sense_intersection)
        if intersection_len > 0:
            edges.append((str(concept["concepticon_id"]), str(other_concept["concepticon_id"]), intersection_len))


    return((cids, glosses, edges))

#creates igraph network, saves it to .gml-file
def build_network(sense, output_file):
    cids, glosses, edges = convert_sense(sense)
    graph = igraph.Graph()
    graph.add_vertices(cids)
    graph.vs["ID"] = cids
    graph.vs["Gloss"] = glosses
    graph.add_edges([(ID, other_ID) for (ID, other_ID, weight) in edges])
    graph.es['weight'] = [weight for ID, other_ID, weight in edges]
    graph.write_gml(output_file)
    return(print("sense network successfully built and saved to " + output_file))

if __name__=="__main__":
    build_network(sense, output_file)
