from pysen.glosses import to_concepticon
from pyconcepticon import Concepticon
import igraph
con = Concepticon()

clics_graph = igraph.read("input/CLICS/network-3-families.gml")
tsv_path = 'output/w2v/mapped_concepts.tsv'
vocab_path = 'output/w2v/model_vocab.txt'

def get_concept_data(conceptlist):
    clics_data = []
    for concept in con.conceptlists[conceptlist].concepts.values():
        if concept.concepticon_id in [concept["ID"] for concept in clics_graph.vs]:
            clics_data += [[concept.concepticon_id, concept.concepticon_gloss, concept.attributes['community'], concept.attributes['weighted_family_degree'], concept.attributes['weighted_language_degree']]]
    return(clics_data)

def map_concepts(vocab_path):
    mapped_concepts = []
    with open(vocab_path, encoding='utf-8') as vocab:
        for word in map(lambda x: x.strip(), vocab):
            mapped = to_concepticon([{'gloss': word}])
            for res in mapped[word]:
                mapped_concepts += [[word]+res]
    return(mapped_concepts)

def compare_concepts(mapped, conceptlist_data):
    shared_concepts = []
    clics_IDs = [ID for [ID, gloss, community, family, language] in conceptlist_data]
    for concept in mapped:
        concepticon_id = concept[1]
        if concepticon_id in clics_IDs:
            shared_concepts.append(concept)
    return(shared_concepts)

def get_shared_concepts(vocab, output_tsv_path):
    #clics_data = get_concept_data('Rzymski-2020-1624')
    shared_concepts = map_concepts(vocab)
    #shared_concepts = compare_concepts(mapped_concepts, clics_data)
    with open(output_tsv_path, 'w') as f:
        f.write('\t'.join(
            [
                'Word', 'Concepticon_ID', 'Concepticon_Gloss',
                'POS', 'Similarity'])+'\n')
        for line in shared_concepts:
            f.write('\t'.join([str(x) for x in line])+'\n')

    return(print('[i] found {0} matches'.format(len(shared_concepts))))

if __name__=='__main__':
    get_shared_concepts(vocab_path, tsv_path)
