#!/usr/bin/env python
# coding: utf-8

# In[6]:


import csv
import re
import gensim
from gensim.models import KeyedVectors
import nltk 
from nltk.stem import WordNetLemmatizer 
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from nltk.corpus import wordnet
from itertools import combinations
from tqdm import tqdm
from pathlib import Path
import io


# In[7]:

corpus = 'input/Brown/brown.csv'
model_path = 'output/w2v/w2v.model'
vocab_path = 'output/w2v/model_vocab.txt'

#create model from pretrained google vectors
Path("output/w2v/google").mkdir(parents=True, exist_ok=True)
google_path = 'input/google_pretrained_w2v/word2vec-google-news-300.gz'
google_vectors = 'output/w2v/google/w2v_google.model'
google_vocab_path = 'output/w2v/google/google_vocab.txt'

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


# In[10]:


def preproc(file):
    lemmatizer = WordNetLemmatizer() 
    lemmatized_files = []
    text_lemmas = []
    last_fn = file[1][0]
    for row in file[1:]:
        lemma_list = []
        fn = row[0]
        pos_text = row[3]
        pos_tokens = pos_text.split()
        for token in pos_tokens:
            token_w_pos = token.split("/")
            token_text = token_w_pos[0]
            token_pos = pos_tagger(token_w_pos[1].upper())
            if re.match("[a-zA-Z]+", token_text):
                token_text = token_text.lower()
                '''
                if token_pos == None:
                    token_lemma = lemmatizer.lemmatize(token_text)
                else:
                    token_lemma = lemmatizer.lemmatize(token_text, token_pos)
                lemma_list.append(token_lemma)
                '''
                lemma_list.append(token_text)
        #if fn == last_fn:
         #   text_lemmas = text_lemmas + lemma_list
        #elif lemma_list != []:
        if lemma_list != []:
            #lemmatized_files.append(text_lemmas)
            #text_lemmas = lemma_list
        #last_fn = fn
            lemmatized_files.append(lemma_list)
    #lemmatized_files.append(text_lemmas)
    return(lemmatized_files)


# In[17]:


def build_model(corpus_path, vector_path, vocab_output_path, window_size = 5, google_vectors = False):
    if google_vectors:
        wv = KeyedVectors.load_word2vec_format(corpus_path, binary=True)
    else:
        with open(corpus_path, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)

        preproc_data = preproc(data)
        model = gensim.models.Word2Vec(preproc_data, window = window_size, size=300, workers=6)
        wv = model.wv
    wv.save(vector_path)
    #model.save(model_output_path)

    vocab = list(wv.vocab)
    print("number of word types: " + str(len(vocab)))
    
    with io.open(vocab_output_path, 'w', encoding="utf-8") as f:
        for item in vocab:
            f.write("%s\n" % item)
    return(print("word types saved to " + vocab_output_path))

def get_most_similar(wv_path, n=10):
    vectors = KeyedVectors.load(wv_path, mmap='r')
    vocab = list(vectors.vocab)
    sim_scores = []
    for w1,w2 in tqdm(combinations(vocab, 2)):
        sim = vectors.similarity(w1,w2)
        sim_scores.append((w1, w2, sim))
    top_10 = sim_scores.sorted(key=lambda x: x[2], reverse=True)[:10]
    print(top_10)



if __name__=="__main__":
    #build_model(corpus, model_path, vocab_path)
    #get_most_similar("output/w2v/wv.wordvectors")
    build_model(google_path, google_vectors, google_vocab_path, google_vectors=True)


# In[ ]:




