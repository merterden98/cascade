# fly_annotate.py
#
# generate annotations on Fly (D. melanogaster) network (and yeast)
#
# TODO: update to output original annotations along with new annotations
import pickle
from src import makegraph
from src import vote
from src import confidence as conf
from src import graph
from src import stats
from src.crossvalidate import *
import sys
import csv

def main(argv):
    from src import makegraph
    from src import vote
    from src import confidence as conf
    from src import graph
    from src import stats
    
    # load graph
    # fly_graph = pickle.load(open("pickles/cdsd_FLY_gobp3_inf_35170.pkl", 'rb'))
    fly_graph = pickle.load(open("pickles/cdsd_FLY_gomfbp3_infL6_35170.pkl", 'rb'))
    # yeast_graph = pickle.load(open("pickles/cdsd_gomfbp3_inf_35170.pkl", 'rb'))
    # yeast_graph = pickle.load(open("pickles/cdsd_gomfbp3_infL4_35170.pkl", 'rb'))
    
    # Prepare graph
    known_nodes = set(fly_graph.training_nodes)
    test_nodes = [n for n in fly_graph.node_list  if n not in known_nodes]
    print("known set size: {} // unknown set size: {}".format(
        len(known_nodes), len(test_nodes))
    )
    cascade.prep_training_labelconf(list(known_nodes))

    # check label stats
    all_labels = set()
    for node in fly_graph.node_list:
        for l in node.labels:
            all_labels.add(l)

    print("total labels: {}".format(len(all_labels)))

    # CASCADE SETTINGS
    # voting_func = vote.mv
    # conf_func = conf.entropy_conf
    # cascade_rounds = 4
    # conf_threshold = 0.35
    # nb_type = "known"
    voting_func = vote.wmv
    conf_func = conf.count_conf
    cascade_rounds = 12
    conf_threshold = 0.35
    nb_type = "known"

    # RUN CASCADE
    cv_round(
        ppigraph=fly_graph,
        test_nodes=test_nodes,
        voting_func=voting_func,
        conf_func=conf_func,
        nb_type=nb_type,
        cascade_rounds=cascade_rounds,
        conf_threshold=conf_threshold,
    )

    output_rows = [["node", "pseudolabel?", "label", "label_conf"]]
    for n in test_nodes:
        name = n.name
        plabel = "Y" if n.pseudo_label else "N"
        labelname = n.predicted_label
        conf_score = n.label_conf
        output_rows.append([name, plabel, n.predicted_label, conf_score])

    num_plabels = sum([1 for n in output_rows if n[1] == "Y"])
    
    print("num plabeled nodes: {} / {}".format(num_plabels, len(test_nodes)))
        
    funcstrings = {
        vote.mv: "MV",
        vote.wmv: "WMV",
        conf.count_conf: "CC",
        conf.entropy_conf: "EC",
        conf.weighted_count_conf: "WCC",
    }

    OUTPUT_DIR = "raw_results/FLY/annotate/test/"
    outfile = "{}/flyAnnotate35170.{}.{}.{}.{}.{}.txt".format(
        OUTPUT_DIR,
        funcstrings[voting_func],
        funcstrings[conf_func],
        str(conf_threshold),
        str(cascade_rounds),
        nb_type
    )

    with open(outfile, 'w') as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(output_rows)


if __name__ == "__main__":
    main(sys.argv)
