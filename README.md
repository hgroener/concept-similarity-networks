# concept similarity networks

## Schritte zur Erstellung des Word2Vec-Netzwerks
- Textkorpus zum Trainieren finden (etwa Brown University Standard Corpus of Present-Day American English: https://www.kaggle.com/nltkdata/brown-corpus?select=cats.csv)
- falls nicht schon geschehen: Preprocessing, Tokenisierung, Lemmatisierung, POS-Tagging durchführen
- Concept-Mapping mit pynorare (Genauigkeit evtl. gesteigert durch POS-Tagging), gemappte Wörter etwa durch "(concept set name: CONCEPT_SET_NAME)" ersetzen
- Word2Vec-Modell auf mit Konzeptnamen ausgezeichnetem, vorverarbeitetem, tokenisiertem Text trainieren
- Mit cosine similiarity zwischen Vektoren, die Konzepte repräsentieren, semantische Ähnlichkeit zwischen allen Konzepten (evtl. in einem Subset der Konzepte auf Concepticon) berechnen 
- Schwelle definieren (etwa 0,5) 
- graphische Darstellung des Netzwerks: Kanten werden nur zwischen Konzeptknoten angezeigt, deren semantische Ähnlichkeit den Schwellenwert übersteigt. 

## Vergleich von Ählichkeitsnetzwerken
- Ähnlichkeit zwischen zwei Netzwerken (mindestens eins davon ungewichtet):
  - Definition eines Schwellenwertes für gewichtete Netzwerke 
  - Anteil der Kanten, die in beiden Netzwerken vorkommen wird prozentual berechnet
- Ähnlichkeit zwischen zwei gewichteten Netzwerken: 
  - für jede Kante Ähnlichkeit auf einen Wert zwischen 0 und 1 normalisieren 
  - Differenz zwischen den normalisierten Ähnlichkeitswerten jeder Kante berechnen
  - "average degree" = Summe der Kanten an jedem Knoten durch die Zahl der Knoten -> Vergleich der Dichte der Netzwerke
- Vergleich konzeptueller Felder: 
  - Anzahl und Größe von Feldern
  - Ähnlichkeit der Felder: 
    - für jedes Feld in einem Netzwerk das ähnlichste in einem anderen Netzwerk suchen 
    - Überlappung (in Konzepten) zwischen den beiden Feldern berechnen
    - Unterschiede, Gemeinsamkeiten, Art der Ähnlichkeit für einzelne Felder beschreiben 
    
## Fragen
- Umgang mit pynorare, pyconcepticon, pyclics
- wie viele und welche Ähnlichkeitsnetzwerke sollten verglichen werden? Nur gewichtete (pyclics, word2vec, evtl. Netzwerk aus Assoziationsstudien in NoRaRe) oder auch ungewichtete (Wordnet, Concepticon)
- Reicht pynorare für das Konzeptmapping, oder sollte für das Mapping bei Kolexifikationen ein Klassifikator eingesetzt werden?


