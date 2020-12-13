#!/usr/bin/env python
# coding: utf-8

# In[6]:


import csv
import re
import gensim 
import spacy
from gensim.models import Word2Vec
import nltk 
from nltk.stem import WordNetLemmatizer 
nltk.download('averaged_perceptron_tagger') 
from nltk.corpus import wordnet 
from nltk.corpus import reuters


# In[7]:


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
                if token_pos == None:
                    token_lemma = lemmatizer.lemmatize(token_text)
                else:
                    token_lemma = lemmatizer.lemmatize(token_text, token_pos)
                lemma_list.append(token_lemma)
        if fn == last_fn:
            text_lemmas = text_lemmas + lemma_list
        elif lemma_list != []:
            lemmatized_files.append(text_lemmas)
            text_lemmas = lemma_list
        last_fn = fn
    lemmatized_files.append(text_lemmas)
    return(lemmatized_files)


# In[17]:


if __name__ == '__main__':
    
    with open('D:/Brown/brown.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    preproc_data = preproc(data)
   
    
    brown_model = gensim.models.Word2Vec(preproc_data, min_count = 1, window = 5)
    brown_vocab = list(brown_model.wv.vocab)
    print("number of word types: " + str(len(brown_vocab)))
    
    with open('model_vocab.txt', 'w') as f:
        for item in brown_vocab:
            f.write("%s\n" % item)
    print("word types saved to model_vocab.txt")


# In[ ]:




