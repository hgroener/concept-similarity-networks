from pysen.glosses import to_concepticon
from pyconcepticon import Concepticon

con = Concepticon()
clics_data = []
for concept in con.conceptlists['Rzymski-2020-1624'].concepts.values():
    clics_data += [[concept.concepticon_id, concept.concepticon_gloss, concept.attributes['community'], concept.attributes['weighted_family_degree'], concept.attributes['weighted_language_degree']]]    

mapped_concepts = []
with open('output/model_vocab.txt') as vocab:
    for word in map(lambda x: x.strip(), vocab):
        mapped = to_concepticon([{'gloss': word}])
        for res in mapped[word]:
            mapped_concepts += [[word]+res]    

shared_concepts = []
clics_IDs = [ID for [ID, gloss, community, family, language] in clics_data]
for concept in mapped_concepts:
    concepticon_id = concept[1]
    if concepticon_id in clics_IDs:
        shared_concepts.append(concept)

with open('output/shared_concepts.tsv', 'w') as f:
    f.write('\t'.join(
        [
            'Word', 'Concepticon_ID', 'Concepticon_Gloss', 
            'POS', 'Similarity'])+'\n')
    for line in shared_concepts:
        f.write('\t'.join([str(x) for x in line])+'\n')

print('[i] found {0} matches'.format(len(shared_concepts)))
