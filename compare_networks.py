import evaluation
import generate_subgraph
import implement_threshold

clics_path = 'input/CLICS/network-3-families.gml'
clics_subgraph_path = 'output/CLICS/clics_subgraph_EAT.gml'
EAT_path = 'output/EAT/EAT_graph.gml'
EAT_subgraph_path = 'output/EAT/EAT_subgraph_CLICS.gml'

def get_graph_stats(graph):
    com_num = len(graph.community_infomap())
    com_size = len(graph.vs) / com_num
    return((com_num, com_size))

def compare_networks(test_path, gold_path, test_model_type, gold_model_type, threshold = 0, w2v=True):
    test_subgraph, gold_subgraph = generate_subgraph.get_subgraphs(test_path, gold_path)
    if w2v == True:
        test_subgraph = implement_threshold.implement_threshold(test_subgraph, threshold)
    result_dic = evaluation.get_result_dic(test_subgraph, gold_subgraph, test_model_type, gold_model_type)
    return(result_dic)

if __name__=="__main__":
    results = compare_networks(clics_path, EAT_path, "CLICS", "EAT", w2v=False)
    for key in results:
        print(key, results[key])