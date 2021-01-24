# run-permute.py
#
# JML, January 2021
import pickle
import numpy as np
from src import makegraph
from src import crossvalidate as cv
from src import cascade
from src import vote
from src import confidence as conf

# ------------------------------------------------------------------
# HARD CODED PPIgraph pickle generation

cdsd_file = "biogrid35170.scerevisiae.cdsd"
labels_file = "scerevisiae_GO_inf.mfbp4.txt"
labels_type = "GO"
metric_type = "DSD"
pickle_file = "yeast-GO-mfbp4.pickle"

# ppi_graph = makegraph.getPPIGraph(
#     cdsd_file,
#     labels_file,
#     labels_type,
#     metric_type,
#     None
# )
# pickle.dump(ppi_graph, open(pickle_file, "wb"))


# ------------------------------------------------------------------
# RUN PERMUTE

# get list of all labels
# all_label_sets = np.array([n.labels for n in ppigraph.training_nodes])

# get list of all labels
# randomly permute
# re-compute training nodes
# assert len(traning_nodes) = 4345
# re-init PPIGraph object
# run CV


def permute_labels(ppg=None):
    """
    Given master/true PPI graph, permute
    the label sets among all nodes and return
    a new PPIgraph object.
    """
    all_labels = np.array([n.labels for n in ppg.node_list])
    permuted_labels = np.random.permutation(all_labels)
        
    # assign permuted label sets to nodes
    for i, n in enumerate(ppg.node_list):
        n.labels = permuted_labels[i]

    ppg.training_nodes = [n for n in ppg.node_list if n.labels != []]
    ppg.unlabelled_nodes = [n for n in ppg.node_list if n.labels == []]

    return ppg


def collect_confs(ppigraph=None):
    correct_confs = []
    
    # Cascade params
    cv_splits = 2
    voting_func = vote.wmv
    conf_func = conf.count_conf
    cascade_rounds = 12
    conf_threshold= 0.35
    nb_type = "known"
    K = 10

    node_list = ppigraph.node_list
    training_list = ppigraph.training_nodes
    training_size = ppigraph.training_size

    # get random ordering of nodes
    node_indices = [i for i in range(training_size)]
    np.random.shuffle(node_indices)
    train_fold_size = training_size // cv_splits

    # Run 2-fold CV
    for i in range(cv_splits):
        
        # Partition nodes into train / test splits
        train_nodes = set([
        training_list[j]
            for j in node_indices[i * train_fold_size:(i + 1) *
                                train_fold_size]
        ])
        test_nodes = [n for n in node_list if n not in train_nodes]
        
        # Prepare label_conf weights for training nodes
        cascade.prep_training_labelconf(list(train_nodes))
        
        # Run a single round of CV
        cv.cv_round(
            ppigraph=ppigraph,
            test_nodes=test_nodes,
            voting_func=voting_func,
            conf_func=conf_func,
            K=K,
            nb_type=nb_type,
            cascade_rounds=cascade_rounds,
            conf_threshold=conf_threshold,
        )
        cascade.reset_pseudolabels(test_nodes)

        # collect correct confidences on test nodes
        for node in test_nodes:
            if not node.labels: continue
            if node.predicted_label in node.labels:
                correct_confs.append(node.label_conf)

        # print accuracy
        print(cv.calc_accuracy(test_nodes))

    return np.array(correct_confs)


if __name__ == "__main__":
    confs_all = []
    confs_pfile = "confs_vals.pickle"

    runs = 50

    for i in range(runs):
        print("permute round {}".format(i+1))
        ppigraph = pickle.load(open(pickle_file, "rb"))
        ppg = permute_labels(ppg=ppigraph)
              
        c = collect_confs(ppg)
        confs_all.extend(c)
        print("conf label size = {}".format(len(c)))
        print("conf mean = {}".format(np.mean(c)))
        print("conf std = {}\n".format(np.std(c)))

    print("overall confidence vals size = {}".format(len(confs_all)))
    pickle.dump(np.array(confs_all), open(confs_pfile, "wb"))
