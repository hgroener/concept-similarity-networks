import igraph
import seaborn as sns
import imgkit
import pandas as pd
import random as rd
import itertools

results = "evaluation/results.csv"
shortened_table = "evaluation/results_short.csv"
fig_path = "evaluation/styled_fig.png"


def get_density(graph):
    possible_edge_len = len(list(itertools.combinations(graph.vs, 2)))
    edge_len = len(graph.es)
    density = edge_len/possible_edge_len
    return(density)

def get_assortativity_table():
    clusters = list(range(1,5)) + ["..."]
    df = pd.DataFrame(columns = clusters, index = clusters)
    for i1,i2 in itertools.combinations_with_replacement(range(1,5), 2):
        random_score = round(rd.uniform(0.002, 0.005), 4)
        if i1 == i2:
            random_score += 0.01
        df[i1][i2] = random_score
        df[i2][i1] = random_score
    df.fillna('', inplace=True)
    return(df)


if __name__=="__main__":
    result_df = pd.read_csv("evaluation/results.csv")
    result_df = result_df.drop(["Unnamed: 0", "nodes compared", "edges compared", "B-cubed p-value", "pairwise evaluation p value",
                                "assortativity p-value", "adjusted rand p-value", "spearman p-value"], axis=1)
    result_df = result_df.rename(columns={"test set": "graph 1", "gold set": "graph 2", "B-cubed score": "B2", "pairwise evaluation score": "PE", "assortativity": "AC",
                                   "adjusted rand coefficient": "ARC", "spearman correlation": "SRC"})

    result_df.to_csv(shortened_table, index=False)
    cmap=sns.diverging_palette(5, 250, as_cmap=True)
    styled_df = result_df.style.background_gradient(cmap=cmap)
    html = styled_df.render()
    imgkit.from_string(html, fig_path)

