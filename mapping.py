from pysem.glosses import to_concepticon
from pyconcepticon import Concepticon
import igraph
con = Concepticon()

tsv_path = 'output/w2v/mapped_concepts.tsv'
vocab_path = 'output/w2v/model_vocab.txt'


def map_concepts(vocab_path):
    mapped_concepts = []
    with open(vocab_path, encoding='utf-8') as vocab:
        for word in map(lambda x: x.strip(), vocab):
            if word != "":
                try:
                    mapped = to_concepticon([{'gloss': word}])
                    for res in mapped[word]:
                        mapped_concepts += [[word]+res]
                except ValueError:
                    print(word + " couldn't be mapped to Concepticon")
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
    shared_concepts = map_concepts(vocab)
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
