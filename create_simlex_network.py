from pyconcepticon import Concepticon
import igraph

output_path = "output/MultiSimLex/MultiSimLex.gml"
concepticon = Concepticon()

# load multisimlex, this is a bit more complex, since we have to get the
# information on the pairings


def create_simlex_network():

    languages = ["english", "russian", "chinese", "cantonese", "arabic", "spanish", "polish", "french", "estonian", "finnish"]

    cl = {concept.number: concept for concept in concepticon.conceptlists["Vulic-2020-2244"].concepts.values()}
    msl = {}
    ids = []
    glosses = []
    for concept in cl.values():
        if not concept.concepticon_id == None:
            ids.append(concept.concepticon_id)
            glosses.append(concept.concepticon_gloss)
            # retrieve all specific values, they are already formatted as a list here
            values = [concept.attributes[attribute] for attribute in ["simlex_ids"] + [language + "_score" for language in languages]]
            # zipping values, means, we tackle them in their order
            for i in range(len(values[0])):
                scores = [values[j][i] for j in range(1, len(values))]
                msl[values[0][i]] = (
                    concept.concepticon_id,
                    concept.concepticon_gloss,
                    sum(scores)/len(scores))

    edges = []
    for i in range(1, len(msl)):
        c1 = str(i) + ':1'
        c2 = str(i) + ':2'
        if c1 in msl and c2 in msl:

            (cidA, cglA, scoreA), (cidB, cglB, scoreB) = msl[str(i) + ':1'], msl[str(i) + ':2']
            assert scoreA == scoreB
            edges.append((cidA, cidB, scoreA))
            # we convert to integer, since the metadata.json does not assign this
            # yet as integer, since it is not yet in norare
            # this can be varied by adding, e.g., weighted_degree as well!


    graph = igraph.Graph()
    graph.add_vertices(ids)
    graph.vs["ID"] = ids
    graph.vs["gloss"] = glosses
    graph.add_edges([(a,b) for (a,b,c) in edges])
    graph.es["weight"] = [c for (a,b,c) in edges]

    return graph

def get_simlex_gml(output_path):
    graph = create_simlex_network()
    graph.write_gml(output_path)
    return(print("MultiSimLex network saved to", simlex_graph))

if __name__ == "__main__":
    get_simlex_gml(output_path)