'''
cascade.py

Module with routines used for cascading procedure.
# NEEDSWORK
'''


def assign_pseudolabels(predictions, test_nodes, conf_cutoff):
    '''
    Assign pseudo labels to nodes with high confidence.
    '''
    high_conf_nodes = [p[0] for p in predictions if p[2] >= conf_cutoff]
    # print("num of conf nodes: {}".format(len(high_conf_nodes)))
    
    for node in high_conf_nodes:
        node.pseudo_label = node.predicted_label
    pruned_test_set = [n for n in test_nodes if n not in high_conf_nodes]
    
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
