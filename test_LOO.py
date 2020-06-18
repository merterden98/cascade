"""
test_LOO.py

Run LOO CV for given ppigraph and voting func.
"""
from datetime import datetime
import numpy as np
import pickle
from src import makegraph
from src import vote
from src import confidence as conf
from src import graph
from src import stats
from src.crossvalidate import *

# ----------------------------------------------------------------------------
#                         LOAD GRAPH PICKLES

# cdsd_gobp3_inf = pickle.load(open("pickles/cdsd_gobp3_inf_35170.pkl", 'rb'))
# cdsd_mips1 = pickle.load(open("pickles/cdsd_mips1_35170.pkl", 'rb'))
# cdsd_mips2 = pickle.load(open("pickles/cdsd_mips2_35170.pkl", 'rb'))
# cdsd_mips3 = pickle.load(open("pickles/cdsd_mips3_35170.pkl", 'rb'))

# cdsd_FLY_gobp3_inf = pickle.load(open("pickles/cdsd_FLY_gobp3_inf_35170.pkl", 'rb'))
# cdsd_FLY_gomfbp3_inf = pickle.load(open("pickles/cdsd_FLY_gomfbp3_inf_35170.pkl", 'rb'))

cdsd_FLY_gomfbp3_inf = pickle.load(open("pickles/cdsd_FLY_gomfbp3_infL6_35170.pkl", 'rb'))
cdsd_gomfbp3_inf = pickle.load(open("pickles/cdsd_gomfbp3_infL6_35170.pkl", 'rb'))


# ----------------------------------------------------------------------------

# graphs = [cdsd_gobp3_inf, cdsd_mips1, cdsd_mips2, cdsd_mips3]
graphs = [cdsd_gomfbp3_inf, cdsd_FLY_gomfbp3_inf]
votes = [vote.mv]

# for graph in graphs:
#     for vote in votes:
#         print("metric: \t{} \tlabels: \t{}".format(graph.metric_type, graph.label_type))
#         print("voting: {}".format(vote))
#         b = run_LOO(
#             ppigraph=graph,
#             voting_func=vote,
#             conf_func=conf.entropy_conf,
#             nb_type='all',
#             conf_threshold=0.3,
#         )
#         print("mean: {}".format(np.mean(b)))
        

#  AVG labels stats
for graph in graphs:
    total_labels = 0
    for node in graph.training_nodes:
        total_labels += len(node.labels)
    total_nodes = len(graph.training_nodes)
    avg_labels = total_labels / total_nodes
    print("metric: \t{} \tlabels: \t{}".format(graph.metric_type, graph.label_type))
    print("total nodes: {} avg labels: {}".format(total_nodes, avg_labels))
    print("total labels: {}".format(total_labels))
        
