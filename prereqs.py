from pathlib import Path
#create file structure
#outputs:
Path("output/w2v").mkdir(parents=True, exist_ok=True)
Path("output/CLICS").mkdir(parents=True, exist_ok=True)
Path("output/EAT").mkdir(parents=True, exist_ok=True)
Path("output/sense").mkdir(parents=True, exist_ok=True)
Path("output/MultiSimLex").mkdir(parents=True, exist_ok=True)
Path("output/1b_words").mkdir(parents=True, exist_ok=True)
#inputs:
Path("input/Brown").mkdir(parents=True, exist_ok=True)
Path("input/CLICS").mkdir(parents=True, exist_ok=True)
Path("input/Concepticon").mkdir(parents=True, exist_ok=True)
Path("input/1b_words").mkdir(parents=True, exist_ok=True)
Path("input/NoRaRe").mkdir(parents=True, exist_ok=True)
Path("input/thematic_relatedness").mkdir(parents=True, exist_ok=True)
