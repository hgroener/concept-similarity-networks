from pyconcepticon import Concepticon
import igraph

output_path = "output/MultiSimLex/MultiSimLex.gml"
concepticon = Concepticon()
languages = ["english", "russian", "chinese", "cantonese", "arabic", "spanish", "polish", "french", "estonian", "finnish"]


# code partly taken from: https://github.com/concepticon/norare-data/blob/master/examples/correlation-simlex-clics.py
def create_simlex_network(languages, return_graph = True):
    print("creating MultiSimLex network...")
    cl = {concept.number: concept for concept in concepticon.conceptlists["Vulic-2020-2244"].concepts.values()}
    msl = {}
    ids = []
    glosses = []
    for concept in cl.values():
        if not concept.concepticon_id == None:
            if not concept.concepticon_id in ids:
                ids.append(concept.concepticon_id)
                glosses.append(concept.concepticon_gloss)

            values = [concept.attributes[attribute] for attribute in ["simlex_ids"] + [language + "_score" for language in languages]]
            for i in range(len(values[0])):
                scores = [values[j][i] for j in range(1, len(values))]
                msl[values[0][i]] = (
                    concept.concepticon_id,
                    concept.concepticon_gloss,
                    sum(scores)/len(scores))

    edges = []
    duplicate_pairs = []
    duplicate_edge_num = 0

    for i in range(1, len(msl)):
        c1 = str(i) + ':1'
        c2 = str(i) + ':2'
        if c1 in msl and c2 in msl:
            (cidA, cglA, scoreA), (cidB, cglB, scoreB) = msl[str(i) + ':1'], msl[str(i) + ':2']
            no_w  = [(a,b) for (a,b,c) in edges]
            assert scoreA == scoreB
            if cidA == cidB:
                duplicate_pairs.append((cidA, cidB, scoreA))
            elif (cidA, cidB) in no_w:
                i = no_w.index((cidA, cidB))
                edges[i] = (cidA, cidB, (edges[i][2] + scoreA)/2)
                duplicate_edge_num += 1
            elif (cidB, cidA) in no_w:
                i = no_w.index((cidB, cidA))
                edges[i] = (cidB, cidA, (edges[i][2] + scoreA)/2)
                duplicate_edge_num += 1
            else:
                edges.append((cidA, cidB, scoreA))


    graph = igraph.Graph()
    graph.add_vertices(ids)
    graph.vs["ID"] = ids
    graph.vs["Gloss"] = glosses
    graph.add_edges([(a,b) for (a,b,c) in edges])
    graph.es["weight"] = [c for (a,b,c) in edges]

    return graph


def get_simlex_gml(languages, output_path):
    graph = create_simlex_network(languages)
    graph.write_gml(output_path)
    return(print("MultiSimLex network saved to", output_path))

if __name__ == "__main__":
    get_simlex_gml(languages, output_path)