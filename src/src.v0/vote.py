"""
vote.py

Module containing variations of majority voting algorithm for function
label predictions.

"""
import numpy as np
import math
from functools import reduce


def vote(ppigraph=None, K=10, predict_nodes=[], voting_func=None,
         conf_func=None, nb_type='all',**kwargs):
    '''
    Wrapper function for managing voting and confidence rating
    procedures.
    '''
    if ppigraph == None:
        raise(Exception("None Graph Provided"))

    node_list = ppigraph.node_list
    node_names = [n.name for n in node_list]
    node_dict = dict(zip(node_names, node_list))

    predictions = []

    for node in predict_nodes:
        if nb_type == 'all':
            t_nearest = [
                n for n in node.sorted_nodes_DSD[1:K+1]
                if node_dict[n] not in predict_nodes
            ] # don't include self
        if nb_type == 'known':
            t_nearest = []; t = 0;
            for n in node.sorted_nodes_DSD:
                if node_dict[n] not in predict_nodes:
                    t_nearest.append(n)
                    t += 1
                if t == K:
                    break            
        
        pred = voting_func(node, t_nearest, node_dict)
        node.predicted_label = pred
        conf = conf_func(node, t_nearest, node_dict)
        node.conf_score = conf
        predictions.append((node,pred,conf))

    return predictions

#Returns a str in the form of a label
def mv(node, neighbors, node_dict, **kwargs):
    '''
    Majority vote algorithm that returns a predicted label for a single node.

    # NEEDSWORK
    '''

    votes = {}

    for nb_name in neighbors:
        nb = node_dict[nb_name]
        nb_labels = nb.labels
        if nb.pseudo_label:
            nb_labels = [nb.pseudo_label]
        for l in nb_labels:
            if l in votes: votes[l] += 1
            else: votes[l] = 1            

    sorted_votes = sorted(
        votes.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    if not sorted_votes: return None

    top_vote_score = sorted_votes[0][1]
    top_labels  = [n[0] for n in sorted_votes if n[1] == top_vote_score]
    top_labels.sort()

    prediction = top_labels[0]
    return prediction


def wmv(node, neighbors, node_dict, **kwargs):
    '''
    Weighted majority vote algorithm that returns a predicted label for a
    single node.
    '''
    votes = {}

    for nb_name in neighbors:
        nb = node_dict[nb_name]
        nb_labels = nb.labels
        nb_weight = 1 / node.dsd_dict[nb_name]
        if nb.pseudo_label:
            nb_labels = [nb.pseudo_label]
        for l in nb_labels:
            if l in votes: votes[l] += nb_weight
            else: votes[l] = nb_weight

    sorted_votes = sorted(
        votes.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    if not sorted_votes: return None

    top_vote_score = sorted_votes[0][1]
    top_labels  = [n[0] for n in sorted_votes if n[1] == top_vote_score]
    top_labels.sort()

    prediction = top_labels[0]
    return prediction


def nbnb_vote(node, neighbors, node_dict):
    '''
    Neighbor-neighbor vote algorithm that returns predicted label
    for a single node.

    #NEEDSWORK
    '''
    votes = {}
    this_neighbors = set(neighbors)

    for nb_name in neighbors:
        nb = node_dict[nb_name]

        nb_neighbors = nb.sorted_nodes_DSD[:11]
        nb_overlap = [n for n in nb_neighbors if n in this_neighbors]
        nb_vote_weight = len(nb_overlap)
        nb_labels = nb.labels
        if nb.pseudo_label:
            nb_labels = [nb.pseudo_label]
        for l in nb_labels:
            if l in votes: votes[l] += nb_vote_weight
            else: votes[l] = nb_vote_weight

    sorted_votes = sorted(
        votes.items(),
        key=lambda x: x[1],
        reverse=True,
    )
    if not sorted_votes: return None

    top_vote_score = sorted_votes[0][1]
    top_labels = [n[0] for n in sorted_votes if n[1] == top_vote_score]
    top_labels.sort()

    prediction = top_labels[0]
    return prediction

