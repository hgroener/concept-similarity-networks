from pysen.glosses import to_concepticon

table = []
with open('model_vocab.txt') as data:
    for word in map(lambda x: x.strip(), data):
        mapped = to_concepticon([{'gloss': word}])
        for res in mapped[word]:
            table += [[word]+res]
with open('mapped.tsv', 'w') as f:
    f.write('\t'.join(
        [
            'Word', 'Concepticon_ID', 'Concepticon_Gloss', 
            'POS', 'Similarity'])+'\n')
    for line in table:
        f.write('\t'.join([str(x) for x in line])+'\n')

print('[i] found {0} matches'.format(len(table)))
