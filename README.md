## Quantitative Concept Similarity: Comparing Similarities Derived from Word Embeddings to Similarities Derived from Cross-Linguistic Data

# README 

Necessary steps before running the code: 

1. Run prereqs.py to create file structure for input and output files 
2. Install pysem from https://github.com/lingpy/pysem
3. Download CLICS .gml-file from https://github.com/clics/clics3/blob/master/clics3-network.gml.zip and unpack it into input/CLICS
4. Clone NoRaRe repository into input/NoRaRe with "git clone https://github.com/concepticon/norare-data"
5. Download Brown corpus from https://www.kaggle.com/nltkdata/brown-corpus?select=brown.csv and extract it into input/Brown
6. Download 1 billion word corpus from http://www.statmt.org/lm-benchmark/1-billion-word-language-modeling-benchmark-r13output.tar.gz, move it to input/1b_words
7. Download thematic relatedness norms from https://static-content.springer.com/esm/art%3A10.3758%2Fs13428-015-0679-8/MediaObjects/13428_2015_679_MOESM2_ESM.xlsx, place the file into input/thematic_relatedness
8. Install all packages listed in requirements.txt
9. add imgkit to Path variable to run visualization.py and export styled tables 

To start the creation and comparison of networks, run main.py. Change the boolean values of "overwrite" and "compare" variables to toggle overwriting and comparing networks.

