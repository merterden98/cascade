"""
vote.py

Module containing variations of majority voting algorithm for function
label predictions.

"""
import numpy as np
import math
from functools import reduce


def vote(ppigraph=None,
         K=10,
         predict_nodes=[],
         voting_func=None,
         conf_func=None,
         nb_type='all',
         c_round=0,
         **kwargs):
    '''
    Wrapper function for managing voting and confidence rating
    procedures.
    '''
    if ppigraph == None:
        raise (Exception("None Graph Provided"))

    node_list = ppigraph.node_list
    node_names = [n.name for n in node_list]
    node_dict = dict(zip(node_names, node_list))

    predictions = []

    predict_node_set = set(predict_nodes)

    # Get t_nearest neighborhood under DSD of node
    for node in predict_nodes:
        if nb_type == 'all':
            t_nearest = [
                n for n in node.sorted_nodes_DSD[1:K + 1]
                if node_dict[n] not in predict_node_set
            ]  # don't include self

        if nb_type == 'known':
            t_nearest = []
            t = 0
            for n in node.sorted_nodes_DSD:
                if node_dict[n] not in predict_node_set:
                    t_nearest.append(n)
                    t += 1
                if t == K:
                    break

        # Use only with hierarchy voting functions; lets us use
        # the labels in higher levels from nodes also in predict_node_set
        if nb_type == 'all_h':
            t_nearest = [n for n in node.sorted_nodes_DSD[1:K + 1]]

        pred = voting_func(node, t_nearest, node_dict)
        node.predicted_label = pred
        conf = conf_func(node, t_nearest, node_dict)
        node.conf_score = conf
        predictions.append((node, pred, conf))

    return predictions


#Returns a str in the form of a label
def mv(node, neighbors, node_dict, **kwargs):
    '''
    Majority vote algorithm that returns a predicted label for a single node.

    NEW (2019.4.22):

    - Nodes vote with a score proportional to their label_conf.
    '''

    # votes = {}
    votes = node.votes

    for nb_name in neighbors:
        nb = node_dict[nb_name]
        nb_labels = nb.labels
        nb_votepower = nb.label_conf
        if nb.pseudo_label:
            nb_labels = [nb.pseudo_label]
        for l in nb_labels:
            if l in votes: votes[l] += nb_votepower
            else: votes[l] = nb_votepower

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


def wmv(node, neighbors, node_dict, **kwargs):
    '''
    Weighted majority vote algorithm that returns a predicted label for a
    single node.
    '''
    # votes = {}]
    votes = node.votes

    for nb_name in neighbors:
        nb = node_dict[nb_name]
        nb_labels = nb.labels

        # DEBUG
        # print("node: {}, nb: {}".format(node.name, nb_name))

        if node.dsd_dict[nb_name] == 0: continue
        nb_votepower = (1 / node.dsd_dict[nb_name]) * nb.label_conf
        if nb.pseudo_label:
            nb_labels = [nb.pseudo_label]
        for l in nb_labels:
            if l in votes: votes[l] += nb_votepower
            else: votes[l] = nb_votepower

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


def mv_hierarchy(node, neighbors, node_dict, **kwargs):
    '''
    Majority vote algorithm using MIPS label hierarchical structure
    '''

    # votes = {}
    votes = node.votes

    aggregate_hierarchy_labels(neighbors, node_dict)

    for nb_name in neighbors:
        nb = node_dict[nb_name]
        nb_labels = nb.labels
        nb_votepower = nb.label_conf
        if nb.pseudo_label:
            nb_labels = [nb.pseudo_label]
        for l in nb_labels:
            if l in votes: votes[l] += nb_votepower
            else: votes[l] = nb_votepower

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


def aggregate_hierarchy_labels(neighbors, node_dict):
    """
        Collates neighbors that do not have 
        higher level labels.
    """
    # Key is label value is count
    hierarchy_labels = {}
    for neighbor in neighbors:
        # Checks if we don't have labels for current node
        if not node_dict[neighbor].labels:
            # We technically have only two levels of MIPS but
            # good to future proof here.
            for combined_label_list in neighbor.hierarchy_labels.values():
                for (_, label_list) in combined_label_list:
                    for label in label_list:
                        if label not in hierarchy_labels:
                            hierarchy_labels[label] = 1
                        else:
                            hierarchy_labels[label] += 1
