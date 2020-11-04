# BA_concept_similarity

##Schritte zur Erstellung des Word2Vec-Netzwerks: 
- Textkorpus zum Trainieren finden (etwa Brown University Standard Corpus of Present-Day American English: https://www.kaggle.com/nltkdata/brown-corpus?select=cats.csv)
- falls nicht schon geschehen: Preprocessing, Tokenisierung, Lemmatisierung, POS-Tagging durchführen
- Concept-Mapping mit pynorare (Genauigkeit evtl. gesteigert durch POS-Tagging), gemappte Wörter etwa durch "(concept set name: CONCEPT_SET_NAME)" ersetzen
- Word2Vec-Modell auf mit Konzeptnamen ausgezeichnetem, vorverarbeitetem, tokenisiertem Text trainieren
- Mit cosine similiarity zwischen Vektoren, die Konzepte repräsentieren, semantische Ähnlichkeit zwischen allen Konzepten (evtl. in einem Subset der Konzepte auf Concepticon) berechnen 
- Schwelle definieren (etwa 0,5) 
- graphische Darstellung des Netzwerks: Kanten werden nur zwischen Konzeptknoten angezeigt, deren semantische Ähnlichkeit den Schwellenwert übersteigt. 

##Vergleich von Ählichkeitsnetzwerken:
- quantitativ
  - Ähnlichkeit zwischen zwei Netzwerken in numerischem Wert: 
    - für jede Kante Ähnlichkeit auf einen Wert zwischen 0 und 1 normalisieren 
    - Ähnlichkeit zweier Netzwerke = Differenz zwischen den normalisierten Ähnlichkeitswerten jeder Kante
  -
