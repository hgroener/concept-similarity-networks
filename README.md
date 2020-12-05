# concept similarity networks

## Schritte zur Erstellung des Word2Vec-Netzwerks
- Textkorpus: Brown University Standard Corpus of Present-Day American English: https://www.kaggle.com/nltkdata/brown-corpus?select=cats.csv
- Preprocessing, Tokenisierung, Lemmatisierung
- Word2Vec-Modell auf vorverarbeitetem, tokenisiertem Text trainieren
- Liste von Worttypen extrahieren (etwa 50 000) 
- Worttypen mit pynorare auf Konzepte in Konzepteliste mappen
- cosine similiarity scores zwischen Vektoren, die gemappte Worttypen repräsentieren, berechnen
- Schwelle definieren (etwa 0,5) 
- 1000 Konzepte mit meisten Verbindungen über Schwellenwert extrahieren(?)
- graphische Darstellung des Netzwerks: Kanten werden nur zwischen Konzeptknoten angezeigt, deren semantische Ähnlichkeit den Schwellenwert übersteigt. (cytoscape/gephi/networkx/python-igraph) 

## Vergleich von Ählichkeitsnetzwerken
- Literatur: List(2019): beyond edit distances; List(2017): Old Chinese Vowel Purity -> Partitionierungsanalyse
- Connected Components: 
  - Communities verbundener Knoten in Netzwerk
  - Infomap-Algorithmus: Labeling der Connected Components (etwa Konzept "GET" in Community "TAKE")
    
## Fragen
- Umgang mit pynorare, pyconcepticon, pyclics
- wie viele und welche Ähnlichkeitsnetzwerke sollten verglichen werden? Nur gewichtete (pyclics, word2vec, evtl. Netzwerk aus Assoziationsstudien in NoRaRe) oder auch ungewichtete (Wordnet, Concepticon)
- Reicht pynorare für das Konzeptmapping, oder sollte für das Mapping bei Kolexifikationen ein Klassifikator eingesetzt werden?


