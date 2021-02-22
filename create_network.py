#!/usr/bin/env python
# coding: utf-8

# In[3]:


import gensim
import csv
import pandas as pd
import networkx as nx
import itertools
from tqdm import tqdm
import matplotlib.pyplot as plt
import random as rd
from pyconcepticon import Concepticon


# In[4]:


def read_mappings(table):
	with open(table) as fd:
		fd.readline()
		rd = csv.reader(fd, delimiter="\t", quotechar='"')
		mapped_vocab = []
		for a, b, c, d, e in rd:
			mapped_vocab.append((a,{"ID": b}))
	return mapped_vocab


# In[5]:


def create_edges(model, vocab, threshold, filename):
    brown_model = gensim.models.Word2Vec.load(model)
    edges = []
    for word, other_word in tqdm(itertools.combinations([a for (a,b) in vocab], 2)):
        similarity = brown_model.wv.similarity(word, other_word)
        if similarity > threshold:
            edges.append((word, other_word, str(similarity)))
    print("edges per node:" + str(len(edges)/len(vocab)))
    with open(filename, 'w') as f:
        for edge in edges:
            f.write("%s\n" % str(edge))
    return edges


# In[6]:


def create_network(vocab, weighted_edges):
    word2vec_graph = nx.Graph()
    word2vec_graph.add_nodes_from(vocab)
    word2vec_graph.add_weighted_edges_from(weighted_edges)
    return word2vec_graph


# In[7]:


if __name__ == "__main__":
    mapped_vocab = read_mappings("output/shared_concepts.tsv")
    edges = create_edges("output/brown_model.model", mapped_vocab, 0.97, "output/edges.txt")
    word2vec_graph = create_network(mapped_vocab, edges)
    nx.write_gml(word2vec_graph, "output/word2vec_graph.gml")


# In[ ]:




