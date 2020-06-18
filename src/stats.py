"""
stats.py

Module for collecting various stats on network.
"""

def label_distr(ppigraph):
    '''
    Returns dictionary of label names, frequencies.
    '''
    label_dist = {}
    for node in ppigraph.node_list:
        
        labels = node.labels
        for l in labels:
            if l in label_dist:
                label_dist[l] += 1
            else:
                label_dist[l] = 1

    return label_dist


def prediction_distr(ppigraph):
    '''
    Returns dictionary of predicted label names, frequencies.
    
    Nodes ppigraph expected to have predicted_label attribute set.
    '''
    pred_dist = {}
    for node in ppigraph.node_list:
        pred = node.predicted_label
        labels = node.labels
        
        if pred not in pred_dist:
            pred_dist[pred] = [0, 0]
        pred_dist[pred][0] += 1
        
        # compute how many predictions were correct 
        if pred in labels:
            pred_dist[pred][1] += 1
            
    return pred_dist

