'''
cascade.py

Module with routines used for cascading procedure.
# NEEDSWORK
'''
import numpy as np
from scipy import stats


def assign_pseudolabels(predictions, test_nodes, conf_cutoff):
    '''
    Assign pseudo labels to nodes with high confidence.

    Assign node.label_conf = conf_score to high confidence nodes
    '''

    pruned_test_set = []
    high_conf_nodes = 0
    conf_vals = []

    for node_tuple in predictions:
        node = node_tuple[0]
        pred = node_tuple[1]
        conf = node_tuple[2]
        if conf >= conf_cutoff:
            high_conf_nodes += 1
            node.pseudo_label = pred
            node.label_conf = conf
            conf_vals.append(conf)
        else:
            pruned_test_set.append(node)

    return pruned_test_set


def compute_cc(predictions, conf_percent=0.30):
    '''
    Computes high-confidence cutoff value given a set of prediction
    confidence scores.

    Predictions must be a list of (node, prediction, confidence) tuples.
    '''
    conf_vals = [p[2] for p in predictions]
    conf_vals.sort(reverse=True)
    conf_index = round(len(conf_vals) * conf_percent)

    if not conf_index:
        return None

    return conf_vals[conf_index]


def compute_conf_percentiles(predictions):
    '''
    Given a list of (node, pred, conf) tuples, converts each
    conf value into a percentile and returns the updated
    set of tuples.
    
    '''
    conf_vals = [p[2] for p in predictions]
    updated_preds = []

    for n, p, c in predictions:
        conf_percentile = stats.percentileofscore(conf_vals, c)
        new_tuple = (n, p, conf_percentile)
        updated_preds.append(new_tuple)

    return updated_preds


def clean_nodes(node_list):
    '''
    Resets the pseudo_label and predicted_label attributes of all
    PPINode objects in node_list.
    '''
    for node in node_list:
        node.pseudo_label = None
        node.predicted_label = None

    return


def reset_pseudolabels(node_list):
    '''
    Resets the pseudo label attribute on PPINodes in node_list for
    the next round of CV.
    '''
    for node in node_list:
        node.pseudo_label = None

    return


def prep_training_labelconf(node_list):
    '''
    Sets label_conf attribute on each PPINode in node_list to 1.0
    '''
    for node in node_list:
        node.label_conf = 1.0

    return
