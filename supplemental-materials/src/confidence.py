"""
confidence.py

Module containing confidence scoring functions.
"""
import numpy as np
import random
from functools import reduce


def random_conf(node, neighbors, node_dict, **kwargs):
    '''
    Random confidence assignment.
    '''
    rand_score = random.randint(0, 100)
    prediction_conf = rand_score / 100
    return prediction_conf


def count_conf(node, neighbors, node_dict, **kwargs):
    '''
    Count Method for confidence rating.
    '''
    pred = node.predicted_label
    total_vote_sum = 0
    pred_score = 0

    for nb_name in neighbors:
        nb = node_dict[nb_name]
        if nb.pseudo_label:
            total_vote_sum += 1
            if pred == nb.pseudo_label:
                pred_score += 1
            continue
        total_vote_sum += len(nb.labels)
        if pred in nb.labels:
            pred_score += 1

    if not total_vote_sum:
        return 0

    prediction_conf = pred_score / total_vote_sum
    return prediction_conf


def weighted_count_conf(node, neighbors, node_dict, **kwargs):
    '''
    Weighted count Method for confidence rating.

    Should be used with WMV
    '''
    pred = node.predicted_label
    total_vote_sum = 0
    pred_score = 0

    for nb_name in neighbors:
        nb = node_dict[nb_name]

        if node.dsd_dict[nb_name] == 0:
            continue
        nb_weight = 1 / node.dsd_dict[nb_name]

        if nb.pseudo_label:
            total_vote_sum += nb_weight
            if pred == nb.pseudo_label:
                pred_score += nb_weight
            continue
        total_vote_sum += (nb_weight * len(nb.labels))
        if pred in nb.labels:
            pred_score += nb_weight

    if not total_vote_sum:
        return 0

    prediction_conf = pred_score / total_vote_sum
    return prediction_conf


def entropy_conf(node, neighbors, node_dict, **kwargs):
    '''
    Entropy-based confidence scoring.

    #NEEDSWORK
    '''

    pred = node.predicted_label
    total_vote_sum = 0
    pred_score = 0
    count_dict = {}

    votes = {}
    for nb_name in neighbors:
        nb = node_dict[nb_name]
        nb_labels = nb.labels
        if nb.pseudo_label:
            nb_labels = [nb.pseudo_label]
        for l in nb_labels:
            if l in votes: votes[l] += 1
            else: votes[l] = 1

    if not votes.values():
        return 0

    maxVotes = reduce(lambda x, y: x + y, votes.values())
    labelsProbability = [val / maxVotes for val in votes.values()]
    uniformProbability = [
        1 / len(labelsProbability) for i in range(len(labelsProbability))
    ]

    entropyTotal = -np.sum(labelsProbability * np.log2(labelsProbability))
    entropyUnif = -np.sum(uniformProbability * np.log2(uniformProbability))

    if not entropyUnif:
        return 1

    # print(1 - (entropyTotal/entropyUnif))
    return (1 - (entropyTotal / entropyUnif))
