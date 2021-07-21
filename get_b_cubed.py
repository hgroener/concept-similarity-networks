import igraph

EAT_path = "output/EAT/EAT_graph.gml"
CLICS_path = "input/CLICS/network-3-families.gml"

def coms_sgraphs(graph):
    coms = graph.community_infomap()
    sgraphs = coms.subgraphs()
    return((coms, sgraphs))

def get_b_cubed(test_graph, gold_graph):
    test_coms, test_sgraphs = coms_sgraphs(test_graph)
    gold_coms, gold_sgraphs = coms_sgraphs(gold_graph)

    p_list = []
    r_list = []
    for v in test_graph.vs:
        intersection = []
        test_com_no = test_coms.membership[v.index]
        test_com = test_sgraphs[test_com_no]

        gold_v = gold_graph.vs.select(lambda vertex: vertex["ID"] == v["ID"])[0]
        gold_coms_no = gold_coms.membership[gold_v.index]
        gold_com = gold_sgraphs[gold_coms_no]

        for v1 in test_com.vs:
            if v1["ID"] in [v2["ID"] for v2 in gold_com.vs]:
                intersection.append(v1)
        p_list.append(len(intersection) / len(test_com.vs))
        r_list.append(len(intersection) / len(gold_com.vs))

    p = sum(p_list)/len(p_list)
    r = sum(r_list)/len(r_list)
    F = (2 * p * r)/(p + r)

    result_dic = {"precision": p, "recall": r, "F-score": F}
    return(result_dic)


if __name__=="__main__":
    EAT = igraph.read(EAT_path)
    CLICS = igraph.rad(CLICS_path)
    print(get_b_cubed(EAT, CLICS))