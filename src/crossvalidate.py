'''
crossvalidate.py

'''
import random
import numpy as np
import os
from datetime import datetime
from . import graph
from . import vote
from . import cascade
from . import confidence as conf

VOTE_MAP = {'MV': vote.mv, 'WMV': vote.wmv,
            'MVH': vote.mv_hierarchy, 'WMVH': vote.wmv_hierarchy}
CONF_MAP = {
    'ENT': conf.entropy_conf,
    'CT': conf.count_conf,
    'WCT': conf.weighted_count_conf
}


def run_kfold_cv(ppigraph,
                 cv_splits=3,
                 voting_func=vote.mv,
                 conf_func=conf.count_conf,
                 K=10,
                 nb_type='all',
                 cascade_rounds=10,
                 conf_threshold=0.30):
    '''
    Run 10 rounds of k-fold cross validation, where the number of test
    instances exceeds the number of training instances.
    '''
    accuracy_scores = []
    f1_scores = []
    node_list = ppigraph.node_list
    training_list = ppigraph.training_nodes
    training_size = ppigraph.training_size

    for r in range(10):
        cv_round_acc = []
        cv_round_f1 = []

        print("CV round: {}/10".format(r + 1))

        # Genearte random partition for CV
        node_indices = [i for i in range(training_size)]
        random.shuffle(node_indices)
        train_fold_size = training_size // cv_splits

        # Manage CV rounds
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
            cv_round(
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

            # calculate accuracy per fold
            fold_acc = calc_accuracy(test_nodes)
            cv_round_acc.append(fold_acc)

            # calculate f1 per fold
            fold_f1 = calc_f1(test_nodes, alpha=3)
            cv_round_f1.append(fold_f1)

        avg_fold_acc = np.mean(cv_round_acc)
        avg_fold_f1 = np.mean(cv_round_f1)
        accuracy_scores.append(avg_fold_acc)
        f1_scores.append(avg_fold_f1)
        cascade.clean_nodes(node_list)

    return [accuracy_scores, f1_scores]


def cv_round(ppigraph=None,
             test_nodes=None,
             voting_func=None,
             conf_func=None,
             K=10,
             nb_type='all',
             cascade_rounds=10,
             conf_threshold=0.30):
    '''
    Make predictions and perform cascading on given set of test set nodes.

    '''
    for r in range(cascade_rounds):

        # clear prediction dict for all test nodes
        for node in test_nodes:
            node.votes = {}

        predictions = vote.vote(
            ppigraph=ppigraph,
            K=10,
            predict_nodes=test_nodes,
            voting_func=voting_func,
            conf_func=conf_func,
            nb_type=nb_type,
            c_round=r,
        )  # returns (node, pred, conf) tuples

        # compute pred conf values into percentiles
        # predictions = cascade.compute_conf_percentiles(predictions)
        # conf_cutoff = 1 - conf_threshold

        conf_cutoff = cascade.compute_cc(predictions,
                                         conf_percent=conf_threshold)
        # Continue to cascade with lowest non-zero conf val if conf_cutoff = 0
        if not conf_cutoff:
            conf_vals = [p[2] for p in predictions if p[2] > 0]
            if not conf_vals:
                break
            conf_vals.sort()
            conf_cutoff = conf_vals[0]

        test_nodes = cascade.assign_pseudolabels(predictions, test_nodes,
                                                 conf_cutoff)

    return conf_cutoff


def calc_accuracy(node_list):
    '''
    Computes accuracy score of predictions for nodes in test set.

    NOTE: Only evaluates nodes with at least 1 true annotation.
    '''
    correct = 0
    num_nodes = 0
    for node in node_list:
        if node.labels:
            num_nodes += 1
            if node.predicted_label in node.labels:
                correct += 1

    return correct / num_nodes


def calc_f1(node_list, alpha=3):
    '''
    Compute F1 score on node_list
    '''
    eval_list = [n for n in node_list if n.labels != None]

    all_true_labels = 0  # sum of true positive, false negatives
    predict = 0  # sum of true positives, false positives
    correct = 0  # true positives

    for n in eval_list:
        all_true_labels += len(n.labels)
        top_preds = top_alpha_preds(n, alpha=3)
        predict += len(top_preds)
        for l in top_preds:
            if l in n.labels:
                correct += 1
    prec = float(correct) / float(predict)
    recall = float(correct) / float(all_true_labels)

    f1 = (2 * prec * recall) / (prec + recall)
    return f1


def calc_f1_OLD(node_list, alpha=3):
    '''
    Compute F1 score on node_list:

    f1 = (2 * precision * recall) / (precision + recall)
    '''
    # top_labels = top_alpha_preds(node_list, alpha)
    all_labels = all_function_labels(node_list)
    eval_list = [n for n in node_list if n.labels != None]

    scores = []
    for l in all_labels:
        prec = calc_precision(eval_list, l, alpha=alpha)
        recall = calc_recall(eval_list, l, alpha=alpha)
        if recall == None or prec == None or (prec + recall) == 0:
            continue
        f1 = (2 * prec * recall) / (prec + recall)
        scores.append(f1)

    # print(scores)
    avg_f1 = np.mean(scores)
    return avg_f1


def all_function_labels(node_list):
    '''
    Return a list of all functional labels among nodes in graph.
    '''
    label_set = set()
    for n in node_list:
        for l in n.labels:
            label_set.add(l)
    return list(label_set)


def top_alpha_preds(node, alpha=3):
    '''
    Count top alpha predicted labels given a node and its vote dict.
    '''
    labels_sorted = sorted([(l, score) for l, score in node.votes.items()],
                           key=lambda x: x[1],
                           reverse=True)
    top_labels = [l[0] for l in labels_sorted[:alpha]]

    # print(labels_sorted)

    return top_labels


def calc_precision(node_list, label, alpha=3):
    '''
    Compute precision on node_list given a label.

    Precision = (# correct predictions for label) 
                / (total # predictions for labeL)
    '''
    true_pos = 0
    false_pos = 0
    for n in node_list:
        top_preds = top_alpha_preds(n, alpha=alpha)

        print(top_preds)
        if label not in top_preds:
            continue
        if label in set(n.labels):
            true_pos += 1
        else:
            false_pos += 1

    if (true_pos + false_pos) == 0:
        return None

    prec = true_pos / (true_pos + false_pos)
    return prec


def calc_recall(node_list, label, alpha=3):
    '''
    Compute recall on node_list given a label.

    Recall = (# correct predictions for label)
             / (# correct preds for label + # true labels with no pred)
    '''
    true_pos = 0
    false_neg = 0
    for n in node_list:
        top_preds = top_alpha_preds(n, alpha=alpha)

        true_label = label in set(n.labels)

        if label in top_preds:
            if true_label:
                true_pos += 1
        if true_label:
            if label not in top_preds:
                false_neg += 1

    if (true_pos + false_neg) == 0:
        recall = None
    else:
        recall = true_pos / (true_pos + false_neg)

    return recall


def run_conf_dist_analysis(ppigraph=None,
                           cv_splits=2,
                           voting_func=vote.mv,
                           conf_func=conf.count_conf,
                           K=10,
                           nb_type='all',
                           cascade_rounds=1,
                           conf_threshold=0.30):
    '''
    Run analysis of confidence scoring distribution for a given CV-fold type.

    #NEEDSWORK
    '''
    node_list = ppigraph.training_nodes  # use only nodes with known annotations
    num_nodes = ppigraph.training_size
    confidence_splits = []
    for r in range(10):
        print("Confidence score distribution analysis, round {}/10".format(r +
                                                                           1))

        node_indices = [i for i in range(num_nodes)]
        random.shuffle(node_indices)
        test_fold_size = num_nodes // cv_splits

        round_high_conf_acc = 0
        round_low_conf_acc = 0
        for i in range(cv_splits):
            train_nodes = set([
                node_list[j] for j in node_indices[i * test_fold_size:(i + 1) *
                                                   test_fold_size]
            ])
            test_nodes = [n for n in node_list if n not in train_nodes]

            cascade.prep_training_labelconf(list(train_nodes))

            print(len(test_nodes))
            conf_cutoff = cv_round(
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

            high_conf_nodes = [
                n for n in test_nodes if n.conf_score >= conf_cutoff
            ]
            low_conf_nodes = [
                n for n in test_nodes if n.conf_score <= conf_cutoff
            ]
            high_conf_correct = 0
            low_conf_correct = 0
            for n in high_conf_nodes:
                if n.predicted_label in n.labels:
                    high_conf_correct += 1
            for n in low_conf_nodes:
                if n.predicted_label in n.labels:
                    low_conf_correct += 1
            round_high_conf_acc += high_conf_correct / len(high_conf_nodes)
            round_low_conf_acc += low_conf_correct / len(low_conf_nodes)

        # Record avg high_conf / low_conf accuracy for the round of CV
        round_high_conf_avg = round_high_conf_acc / cv_splits
        round_low_conf_avg = round_low_conf_acc / cv_splits
        confidence_splits.append((round_high_conf_avg, round_low_conf_avg))
        cascade.clean_nodes(node_list)

    return confidence_splits


def generate_filename(voting_func,
                      conf_func,
                      threshold,
                      labels,
                      folds,
                      nb_type,
                      casc_rounds,
                      metric="DSD"):
    vote = voting_func
    conf = conf_func
    threshold *= 100
    fname = "acc.{}.{}.{}.{}.{}.{}r.{}f.{}.txt".format(labels, metric, vote,
                                                       conf, int(threshold),
                                                       casc_rounds, folds,
                                                       nb_type)
    return fname


def output_results(ofname, **kwargs):
    f = open(ofname, 'w')
    s = ""
    s += "MVC - Accuracy Results\n"
    s += "{}\n\n".format(datetime.now())
    s += "Graph type:\tS. Cerevisiae\nMetric:\t{}\n\n".format(
        kwargs['ppigraph'])
    s += "Labels\t {}\n\n".format(kwargs['labels'])
    s += "Voting algorithm:\t{}\n".format(kwargs['voting_func'])
    s += "Neighbor type:\t{}\n".format(kwargs['nb_type'])
    s += "CV splits:\t{}\n".format(kwargs['cv_splits'])
    s += "Conf. algorithm:\t{}\n".format(kwargs['conf_func'])
    s += "Conf. threshold:\t{}\n".format(kwargs['conf_threshold'])
    s += "Cascade rounds: \t{}\n\n".format(kwargs['cascade_rounds'])
    s += "Average accuracy: \t{}\n".format(kwargs['avg_acc'])
    s += "Std dev accuracy: \t{}\n\n".format(kwargs['std_acc'])
    s += "Average F1 score: \t{}\n".format(kwargs['avg_f1'])
    s += "Std dev F1 score: \t{}\n\n".format(kwargs['std_f1'])
    s += "Acc. values measured using 10 rounds of CV\n"
    f.write(s)
    f.close()
    return


def predict(ppigraph=None,
            voting_type=None,
            conf_type=None,
            K=10,
            nb_type='all',
            cascade_rounds=10,
            conf_threshold=0.30):

    unlabelled_nodes = ppigraph.get_unlabelled_nodes()
    voting_func = VOTE_MAP[voting_type]
    conf_func = CONF_MAP[conf_type]

    for r in range(cascade_rounds):

        # clear prediction dict for all test nodes
        for node in unlabelled_nodes:
            node.votes = {}

        predictions = vote.vote(
            ppigraph=ppigraph,
            K=10,
            predict_nodes=unlabelled_nodes,
            voting_func=voting_func,
            conf_func=conf_func,
            nb_type=nb_type,
            c_round=r,
        )  # returns (node, pred, conf) tuples

        conf_cutoff = cascade.compute_cc(predictions,
                                         conf_percent=conf_threshold)

        if not conf_cutoff:
            conf_vals = [p[2] for p in predictions if p[2] > 0]
            if not conf_vals:
                break
            conf_vals.sort()
            conf_cutoff = conf_vals[0]

        unlabelled_nodes = cascade.assign_pseudolabels(predictions,
                                                       unlabelled_nodes,
                                                       conf_cutoff)
    return {node.name: node.predicted_label for node in unlabelled_nodes}


def run_cv_tests(ppigraph=None,
                 voting_type=None,
                 conf_type=None,
                 K=10,
                 outfile='./',
                 nb_type='all',
                 cascade_rounds=10,
                 conf_threshold=0.30,
                 cv_splits=2,
                 labels=None):

    print(
        "Running acc test for: {} - {} - {} - {} - {} - {}r - {}f - {}".format(
            ppigraph.metric_type,
            labels,
            voting_type,
            conf_type,
            conf_threshold,
            cascade_rounds,
            cv_splits,
            nb_type,
        ))
    ofname = generate_filename(
        voting_type,
        conf_type,
        conf_threshold,
        labels,
        cv_splits,
        nb_type,
        cascade_rounds,
        metric=ppigraph.metric_type,
    )
    ofname = "{}{}".format(outfile, ofname)

    res = run_kfold_cv(ppigraph,
                       cv_splits=cv_splits,
                       voting_func=VOTE_MAP[voting_type],
                       conf_func=CONF_MAP[conf_type],
                       K=K,
                       nb_type=nb_type,
                       cascade_rounds=cascade_rounds,
                       conf_threshold=conf_threshold)

    acc_scores = res[0]
    f1_scores = res[1]
    """
        Below is preamble for printing results
    """
    kwargs = {}
    kwargs['ppigraph'] = ppigraph.metric_type
    kwargs['labels'] = labels
    kwargs['voting_func'] = voting_type
    kwargs['conf_func'] = conf_type
    kwargs['conf_threshold'] = conf_threshold
    kwargs['nb_type'] = nb_type
    kwargs['cascade_rounds'] = cascade_rounds
    kwargs['cv_splits'] = cv_splits
    kwargs['avg_acc'] = np.mean(acc_scores)
    kwargs['std_acc'] = np.std(acc_scores)
    kwargs['avg_f1'] = np.mean(f1_scores)
    kwargs['std_f1'] = np.std(f1_scores)
    print("acc_mean: {}, acc_std: {} // f1_mean: {}, f1_std: {}".format(
        round(np.mean(acc_scores), 4), round(np.std(acc_scores), 4),
        round(np.mean(f1_scores), 4), round(np.std(f1_scores), 4)))

    output_results(ofname, **kwargs)
