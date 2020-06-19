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

    # votes is a dictionary of dictionaries. votes[level][node] == [labels]
    votes = node.votes

    # Indicates how much of the predecessor's vote is passed onto the
    # labeled descendent (the remaining is distributed among the other descendents
    """
        Let's make this a kwarg
    """
    vote_weight = 0.8

    # top_level == 2
    top_level = max(node.hierarchy_labels.keys())
    hvotes = dict()
    for i in range(top_level + 1):
        hvotes[i] = dict()

    for nb_name in neighbors:
        nb = node_dict[nb_name]
        nb_labels = nb.labels
        nb_votepower = nb.label_conf

        top_labels = nb.hierarchy_labels[top_level]
        for l in top_labels:
            if l in hvotes[top_level]:
                hvotes[top_level][l] += 1.0
            else:
                hvotes[top_level][l] = 1.0  # *nb_votepower???
            # descendents = nb.graph.label_descendents[l]

            mvh_recur(nb, l, hvotes, top_level, 1.0,
                      vote_weight)  # consider votepower for pseudolabels

        if nb.pseudo_label:
            curr_level = 0
            h_pseudo_labels = []
            curr_label = nb.pseudo_label
            while curr_level <= top_level:
                h_pseudo_labels.append(curr_label)
                if curr_level < top_level:
                    curr_label = nb.graph.label_predecessors[curr_label]
                curr_level += 1

            # hvotes
            mvh_recur_p(nb, curr_label, hvotes, top_level, nb_votepower,
                        vote_weight, h_pseudo_labels)

    if neighbors:
        for l, v in hvotes[0].items():
            votes[l] = v
    # votes = hvotes[0]
    # print(votes)
    sorted_votes = sorted(
        votes.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    if not sorted_votes: return None

    top_vote_score = sorted_votes[0][1]
    top_labels = [n[0] for n in sorted_votes if n[1] == top_vote_score]
    top_labels.sort()

    #print(sorted_votes)
    prediction = top_labels[0]
    return prediction


def wmv_hierarchy(node, neighbors, node_dict, **kwargs):
    '''
    Majority vote algorithm using MIPS label hierarchical structure
    '''

    # votes is a dictionary of dictionaries. votes[level][node] == [labels]
    votes = node.votes

    # Indicates how much of the predecessor's vote is passed onto the
    # labeled descendent (the remaining is distributed among the other descendents
    vote_weight = 0.8

    # top_level == 2
    top_level = max(node.hierarchy_labels.keys())
    hvotes = dict()
    for i in range(top_level + 1):
        hvotes[i] = dict()

    for nb_name in neighbors:
        nb = node_dict[nb_name]
        nb_labels = nb.labels
        nb_votepower = (1 / node.dsd_dict[nb_name]) * nb.label_conf

        top_labels = nb.hierarchy_labels[top_level]
        for l in top_labels:
            if l in hvotes[top_level]:
                hvotes[top_level][l] += (1 / node.dsd_dict[nb_name])
            else:
                hvotes[top_level][l] = (1 / node.dsd_dict[nb_name])
            # descendents = nb.graph.label_descendents[l]

            mvh_recur(nb, l, hvotes, top_level, 1 / node.dsd_dict[nb_name],
                      vote_weight)  # consider votepower for pseudolabels

        if nb.pseudo_label:
            curr_level = 0
            h_pseudo_labels = []
            curr_label = nb.pseudo_label
            while curr_level <= top_level:
                h_pseudo_labels.append(curr_label)
                if curr_level < top_level:
                    curr_label = nb.graph.label_predecessors[curr_label]
                curr_level += 1

            # hvotes
            mvh_recur_p(nb, curr_label, hvotes, top_level, nb_votepower,
                        vote_weight, h_pseudo_labels)

    if neighbors:
        for l, v in hvotes[0].items():
            votes[l] = v
    # votes = hvotes[0]
    # print(votes)
    sorted_votes = sorted(
        votes.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    if not sorted_votes: return None

    top_vote_score = sorted_votes[0][1]
    top_labels = [n[0] for n in sorted_votes if n[1] == top_vote_score]
    top_labels.sort()

    #print(sorted_votes)
    prediction = top_labels[0]
    return prediction


def mvh_recur(curr_node, pred_label, hvotes, curr_level, curr_votepower,
              vote_weight):
    '''
    Recursively assigns voting power to a label and its descendents
    Takes the top level label as an argument
    '''
    # CHECK THIS
    if curr_level > 0:
        descendents = curr_node.graph.label_descendents[pred_label]
        # Number of descendent labels that belong to the node
        labeled_desc = len([
            x for x in descendents if x in curr_node.hierarchy_labels.values()
        ])
        for d_label in descendents:
            # If the current node is annotated with d_label
            if d_label in curr_node.hierarchy_labels[curr_level - 1]:
                if len(descendents) > 1:
                    vpower = curr_votepower * (vote_weight +
                                               (labeled_desc - 1) *
                                               (1 - vote_weight) /
                                               (len(descendents) - 1))
                else:
                    vpower = curr_votepower * vote_weight
            else:
                if len(descendents) > 1:
                    if labeled_desc > 0:
                        vpower = curr_votepower * labeled_desc * (
                            1 - vote_weight) / (len(descendents) - 1)
                    else:
                        vpower = curr_votepower * (
                            1 - vote_weight) / len(descendents)
                else:
                    vpower = curr_votepower * (1 - vote_weight)
            if d_label in hvotes[curr_level - 1]:
                hvotes[curr_level - 1][d_label] += vpower
            else:
                hvotes[curr_level - 1][d_label] = vpower

            #print("{}: {}".format(d_label, hvotes[curr_level - 1][d_label]))
            mvh_recur(curr_node, d_label, hvotes, curr_level - 1, vpower,
                      vote_weight)


def mvh_recur_p(curr_node, pred_label, hvotes, curr_level, curr_votepower,
                vote_weight, pseudo):
    '''
    Recursively assigns voting power to a pseudo-label and its predecessors.
    Works just as the mvh_recur function, but it checks the list of pseudo labels
    rather than the node's actual labels
    '''

    if curr_level > 0:
        descendents = curr_node.graph.label_descendents[pred_label]
        # Number of descendent labels that belong to the node
        labeled_desc = len([x for x in descendents if x in pseudo])
        # print('descendents: {}'.format(descendents))
        # print('labels: {}'.format(curr_node.hierarchy_labels))
        for d_label in descendents:
            # If the current node is annotated with d_label
            if d_label in pseudo:
                if len(descendents) > 1:
                    vpower = curr_votepower * (vote_weight +
                                               (labeled_desc - 1) *
                                               (1 - vote_weight) /
                                               (len(descendents) - 1))
                else:
                    vpower = curr_votepower * vote_weight
            else:
                if len(descendents) > 1:
                    if labeled_desc > 0:
                        vpower = curr_votepower * labeled_desc * (
                            1 - vote_weight) / (len(descendents) - 1)
                    else:
                        vpower = curr_votepower * (
                            1 - vote_weight) / len(descendents)
                else:
                    vpower = curr_votepower * (1 - vote_weight)
            if d_label in hvotes[curr_level - 1]:
                hvotes[curr_level - 1][d_label] += vpower
            else:
                hvotes[curr_level - 1][d_label] = vpower

            #print("{}: {}".format(d_label, hvotes[curr_level - 1][d_label]))
            mvh_recur_p(curr_node, d_label, hvotes, curr_level - 1, vpower,
                        vote_weight, pseudo)
