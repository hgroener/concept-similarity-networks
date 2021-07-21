import csv
import re
import gensim
import nltk
from nltk.stem import WordNetLemmatizer 
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from nltk.corpus import wordnet
from tqdm import tqdm
import io
import tarfile
import os
import random as rd

#corpora
brown_corpus = 'input/Brown/brown.csv'
billion_words_zipped = "input/1b_words/1-billion-word-language-modeling-benchmark-r13output.tar.gz"
billion_words_corpus = "output/1b_words/1-billion-word-language-modeling-benchmark-r13output/training-monolingual.tokenized.shuffled"

#outputs
vector_path = 'output/w2v/w2v.wordvectors'
vocab_path = 'output/w2v/w2v_vocab.txt'


def pos_tagger(nltk_tag): 
    if nltk_tag.startswith('J'): 
        return wordnet.ADJ 
    elif nltk_tag.startswith('V'): 
        return wordnet.VERB 
    elif nltk_tag.startswith('N'): 
        return wordnet.NOUN 
    elif nltk_tag.startswith('R'): 
        return wordnet.ADV 
    else:           
        return None

def lemmatize_token(token, POS, lemmatizer):
    if POS == None:
        token_lemma = lemmatizer.lemmatize(token)
    else:
        token_lemma = lemmatizer.lemmatize(token, POS)
    return(token_lemma)


def preproc_brown(filename, lemmatize=False):
    lemmatizer = WordNetLemmatizer() 
    sents = []

    with open(filename) as file:
        reader = csv.reader(file)
        for row in list(reader)[1:]:
            sent = []
            pos_text = row[3]
            pos_tokens = pos_text.split()
            for token in pos_tokens:
                token_w_pos = token.split("/")
                token_text = token_w_pos[0]
                token_pos = pos_tagger(token_w_pos[1].upper())
                if re.match("[a-zA-Z]+", token_text):
                    token_text = token_text.lower()
                    if lemmatize:
                        token_text = lemmatize_token(token_text, token_pos, lemmatizer)

                    sent.append(token_text)

            if sent != []:
                sents.append(sent)
    print("size of Brown corpus: {0} sentences and {1} words".format(len(sents), len(sum(sents, []))))
    return(sents)


def preproc_1_b_words(basepath, n = 10, alphabetic=False):
    sentences = []
    print("reading and preprocessing files from 1 billion words corpus...")
    dir = os.listdir(basepath)
    rd.shuffle(dir)
    word_count = 0
    for entry in tqdm(dir[:n]):
        with open(basepath + "/" + entry, encoding="UTF-8") as file:
            for line in file.readlines():
                sent = line.split()
                if alphabetic:
                    sent = [tok.lower() for tok in sent if re.match("^[a-zA-Z]+$",tok)]
                word_count += len(sent)
                sentences.append(sent)
    print("size of subset of 1 billion words corpus: {0} sentences and {1} words".format(len(sentences), word_count))
    return(sentences)


def build_model(brown_corpus, billion_word_corpus,  vector_path, vocab_output_path, window_size=2):
    brown_sents = preproc_brown(brown_corpus)
    billion_word_sents = preproc_1_b_words(billion_word_corpus)
    sents = brown_sents + billion_word_sents
    print("training Word2Vec model...")
    model = gensim.models.Word2Vec(sents, window=window_size, size=300, workers=6)
    wv = model.wv
    wv.save(vector_path)

    vocab = list(wv.vocab)
    print("number of word types: " + str(len(vocab)))
    save_vocab(vocab, vocab_output_path)

    return(print("model successfully built, vectors saved to", vector_path))



def save_vocab(vocab, path):
    with io.open(path, 'w', encoding="utf-8") as f:
        for item in vocab:
            f.write("%s\n" % item)
    return(print("vocab saved to", path))


if __name__=="__main__":
    if not os.path.isfile(billion_words_corpus):
        tar = tarfile.open(billion_words_zipped, "r:gz")
        tar.extractall(path="output/1_b_words")
    build_model(brown_corpus, billion_words_corpus, vector_path, vocab_path)




