"""
test_acc.py

Script for testing accuracy of combinations of voting alg / conf alg / 
cascading procedure.

"""
from datetime import datetime
import numpy as np
import pickle
from src import makegraph
from src import vote
from src import confidence as conf
from src import graph
from src.crossvalidate import *
import sys

# ----------------------------------------------------------------------------
#                         LOAD GRAPH PICKLES


def run_combo(**kwargs):
    a = run_kfold_cv(
        ppigraph=kwargs['ppigraph'],
        cv_splits=kwargs['cv_splits'],
        voting_func=kwargs['voting_func'],
        conf_func=kwargs['conf_func'],
        nb_type=kwargs['nb_type'],
        cascade_rounds=kwargs['cascade_rounds'],
        conf_threshold=kwargs['conf_threshold'],
    )

    acc_scores = a[0]
    f1_scores = a[1]

    kwargs['avg_acc'] = np.mean(acc_scores)
    kwargs['std_acc'] = np.std(acc_scores)
    kwargs['avg_f1'] = np.mean(f1_scores)
    kwargs['std_f1'] = np.std(f1_scores)
    print("acc_mean: {}, acc_std: {} // f1_mean: {}, f1_std: {}".format(
        round(np.mean(acc_scores), 4), round(np.std(acc_scores), 4),
        round(np.mean(f1_scores), 4), round(np.std(f1_scores), 4)))

    return kwargs


def output_results(ofname, **kwargs):
    f = open(ofname, 'w')
    s = ""
    s += "MVC - Accuracy Results\n"
    s += "{}\n\n".format(datetime.now())
    s += "Graph type:\tS. Cerevisiae\nMetric:\t{}\n\n".format(
        kwargs['ppigraph'].metric_type)
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


func_names = {
    vote.mv: "MV",
    vote.wmv: "WMV",
    vote.mv_hierarchy: "MV_H",
    vote.wmv_hierarchy: "WMV_H",
    conf.count_conf: "CC",
    conf.weighted_count_conf: "WCC",
    conf.entropy_conf: "EC",
    conf.random_conf: "RC",
}


def generate_filename(voting_func,
                      conf_func,
                      threshold,
                      labels,
                      folds,
                      nb_type,
                      casc_rounds,
                      metric="DSD"):
    vote = func_names[voting_func]
    conf = func_names[conf_func]
    threshold *= 100
    fname = "acc.{}.{}.{}.{}.{}.{}r.{}f.{}.txt".format(labels, metric, vote,
                                                       conf, int(threshold),
                                                       casc_rounds, folds,
                                                       nb_type)
    return fname


def main(argv):
    from datetime import datetime
    import numpy as np
    import pickle
    from src import makegraph
    from src import vote
    from src import confidence as conf
    from src import graph
    import sys

    flight = int(argv[1])
    print(flight)

    ## GET GRAPHS
    # cdsd_gobp3_inf = pickle.load(open("pickles/cdsd_gobp3_inf_35170.pkl", 'rb'))
    # cdsd_mips1 = pickle.load(open("pickles/cdsd_mips1_35170.pkl", 'rb'))
    # cdsd_mips2 = pickle.load(open("pickles/cdsd_mips2_35170.pkl", 'rb'))
    # cdsd_mips3 = pickle.load(open("pickles/cdsd_mips3_35170.pkl", 'rb'))
    # cdsd_FLY_gobp3_inf = pickle.load(open("pickles/cdsd_FLY_gobp3_inf_35170.pkl", 'rb'))
    # cdsd_FLY_gomfbp3_inf = pickle.load(open("pickles/cdsd_FLY_gomfbp3_inf_35170.pkl", 'rb'))
    # cdsd_gomfbp3_inf = pickle.load(open("pickles/cdsd_gomfbp3_inf_35170.pkl", 'rb'))

    # GO MFBP-4
    # cdsd_gomfbp3_l4_inf = pickle.load(open("pickles/cdsd_gomfbp3_infL4_35170.pkl", 'rb'))
    # cdsd_FLY_gomfbp3_l4_inf = pickle.load(open("pickles/cdsd_FLY_gomfbp3_infL4_35170.pkl", 'rb'))

    # cdsd_gomfbp3_l4_inf_str = pickle.load(open("cdsd_gomfbp3_infL4_4932.pkl", 'rb'))

    # GO MFBP-5 / GO MFBP-6
    # cdsd_gomfbp3_l5_inf = pickle.load(open("pickles/cdsd_gomfbp3_infL5_35170.pkl", 'rb'))
    # cdsd_gomfbp3_l6_inf = pickle.load(open("pickles/cdsd_gomfbp3_infL6_35170.pkl", 'rb'))
    # cdsd_FLY_gomfbp3_l5_inf = pickle.load(open("pickles/cdsd_FLY_gomfbp3_infL5_35170.pkl", 'rb'))
    # cdsd_FLY_gomfbp3_l6_inf = pickle.load(open("pickles/cdsd_FLY_gomfbp3_infL6_35170.pkl", 'rb'))

    # ------ SUPP TABLES: YEAST -------

    if flight == 10:
        cdsd_mips1 = pickle.load(open("pickles/cdsd_mips1_35170.pkl", 'rb'))
        print("# FLIGHT 1: yeast - MIPS1 - EC - baseline")
        folds = [2, 4, 6]
        graph_objs = [cdsd_mips1]
        voting_funcs = [vote.mv, vote.wmv]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [1]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight10/"

    if flight == 11:
        cdsd_mips1 = pickle.load(open("pickles/cdsd_mips1_35170.pkl", 'rb'))
        print("# FLIGHT 1: yeast - MIPS1 - EC - cascade")
        folds = [2, 4, 6]
        graph_objs = [cdsd_mips1]
        voting_funcs = [vote.mv, vote.wmv]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [12]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight11/"

    if flight == 20:
        print("# FLIGHT 2: yeast - MIPS2 - EC - baseline")
        cdsd_mips2 = pickle.load(open("pickles/cdsd_mips2_35170.pkl", 'rb'))
        folds = [2, 4, 6]
        graph_objs = [cdsd_mips2]
        voting_funcs = [vote.mv, vote.wmv]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [1]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight20/"

    if flight == 21:
        print("# FLIGHT 2: yeast - MIPS2 - EC - cascade")
        cdsd_mips2 = pickle.load(open("pickles/cdsd_mips2_35170.pkl", 'rb'))
        folds = [2, 4, 6]
        graph_objs = [cdsd_mips2]
        voting_funcs = [vote.mv, vote.wmv]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [12]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight21/"

    if flight == 30:
        cdsd_mips3 = pickle.load(open("pickles/cdsd_mips3_35170.pkl", 'rb'))
        print("# FLIGHT 3: yeast - MIPS3 - EC - baseline")
        folds = [2, 4, 6]
        graph_objs = [cdsd_mips3]
        voting_funcs = [vote.mv, vote.wmv]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [1]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight30/"

    if flight == 31:
        cdsd_mips3 = pickle.load(open("pickles/cdsd_mips3_35170.pkl", 'rb'))
        print("# FLIGHT 3: yeast - MIPS3 - EC - cascade")
        folds = [6]
        graph_objs = [cdsd_mips3]
        voting_funcs = [vote.wmv]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [12]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight31/"

    if flight == 40:
        print("# FLIGHT 4: yeast - GOmfbp_l4 - EC - baseline")
        cdsd_gomfbp3_inf = pickle.load(
            open("pickles/cdsd_gomfbp3_inf_35170.pkl", 'rb'))
        folds = [2, 4, 6]
        graph_objs = [cdsd_gomfbp3_inf]
        voting_funcs = [vote.mv, vote.wmv]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [1]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight40/"

    if flight == 41:
        cdsd_gomfbp3_inf = pickle.load(
            open("pickles/cdsd_gomfbp3_inf_35170.pkl", 'rb'))
        print("# FLIGHT 4: yeast - GOmfbp_l4 - EC - cascade")
        folds = [2, 4, 6]
        graph_objs = [cdsd_gomfbp3_inf]
        voting_funcs = [vote.mv, vote.wmv]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [12]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight41/"

    if flight == 50:
        print("# FLIGHT 4: fly - GOmfbp_l4 - EC - baseline")
        cdsd_FLY_gomfbp3_inf = pickle.load(
            open("pickles/cdsd_FLY_gomfbp3_inf_35170.pkl", 'rb'))
        folds = [2, 4, 6]
        graph_objs = [cdsd_FLY_gomfbp3_inf]
        voting_funcs = [vote.mv, vote.wmv]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [1]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight50/"

    if flight == 51:
        print("# FLIGHT 4: fly - GOmfbp_l4 - EC - cascade")
        cdsd_FLY_gomfbp3_inf = pickle.load(
            open("pickles/cdsd_FLY_gomfbp3_inf_35170.pkl", 'rb'))
        folds = [2, 4, 6]
        graph_objs = [cdsd_FLY_gomfbp3_inf]
        voting_funcs = [vote.mv, vote.wmv]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [12]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight51/"

    if flight == 60:
        print("# FLIGHT 6: fly - GOmfbp_l4 - EC - baseline")
        cdsd_FLY_gomfbp3_inf = pickle.load(
            open("pickles/cdsd_FLY_gomfbp3_inf_35170.pkl", 'rb'))
        folds = [2, 4, 6]
        graph_objs = [cdsd_FLY_gomfbp3_inf]
        voting_funcs = [vote.mv, vote.wmv]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [1]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight60/"

    if flight == 61:
        print("# FLIGHT 6: fly - GOmfbp_l4 - EC - cascade")
        cdsd_FLY_gomfbp3_inf = pickle.load(
            open("pickles/cdsd_FLY_gomfbp3_inf_35170.pkl", 'rb'))
        folds = [2, 4, 6]
        graph_objs = [cdsd_FLY_gomfbp3_inf]
        voting_funcs = [vote.mv, vote.wmv]
        conf_funcs = [conf.count_conf]
        conf_thresholds = [0.35]
        casc_rounds = [10]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight61/"

    # SUPP TABLES
    if flight == 70:
        cdsd_mips1 = pickle.load(open("pickles/cdsd_mips1_35170.pkl", 'rb'))
        cdsd_mips2 = pickle.load(open("pickles/cdsd_mips2_35170.pkl", 'rb'))
        cdsd_mips3 = pickle.load(open("pickles/cdsd_mips3_35170.pkl", 'rb'))
        cdsd_gomfbp3_inf = pickle.load(
            open("pickles/cdsd_gomfbp3_inf_35170.pkl", 'rb'))
        print("# SUPP FLIGHT: yeast - CC - 12 - 35%")
        folds = [2, 4, 6]
        graph_objs = [cdsd_mips1, cdsd_mips2, cdsd_mips3, cdsd_gomfbp3_inf]
        voting_funcs = [vote.mv, vote.wmv]
        conf_funcs = [conf.count_conf]
        conf_thresholds = [0.35]
        casc_rounds = [12]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight70/"

    if flight == 71:
        cdsd_mips1 = pickle.load(open("pickles/cdsd_mips1_35170.pkl", 'rb'))
        cdsd_mips2 = pickle.load(open("pickles/cdsd_mips2_35170.pkl", 'rb'))
        cdsd_mips3 = pickle.load(open("pickles/cdsd_mips3_35170.pkl", 'rb'))
        cdsd_gomfbp3_inf = pickle.load(
            open("pickles/cdsd_gomfbp3_inf_35170.pkl", 'rb'))
        print("# SUPP FLIGHT: yeast - CC - 12 - 35%")
        folds = [2, 4, 6]
        graph_objs = [cdsd_mips1, cdsd_mips2, cdsd_mips3, cdsd_gomfbp3_inf]
        voting_funcs = [vote.mv, vote.wmv]
        conf_funcs = [conf.weighted_count_conf]
        conf_thresholds = [0.35]
        casc_rounds = [12]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight71/"

    # STRING DATABASE
    if flight == 80:
        print("# FLIGHT 8: yeast - GOmfbp_l4 - EC - baseline")
        cdsd_gomfbp3_l4_inf_str = pickle.load(
            open("cdsd_gomfbp3_infL4_4932.pkl", 'rb'))
        folds = [2, 4, 6]
        graph_objs = [cdsd_gomfbp3_l4_inf_str]
        voting_funcs = [vote.mv, vote.wmv]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [1]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight80/"

    if flight == 81:
        print("# FLIGHT 8: yeast - GOmfbp_l4 - EC - cascade")
        cdsd_gomfbp3_l4_inf_str = pickle.load(
            open("cdsd_gomfbp3_infL4_4932.pkl", 'rb'))
        folds = [2, 4, 6]
        graph_objs = [cdsd_gomfbp3_l4_inf_str]
        voting_funcs = [vote.mv, vote.wmv]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [12]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight81/"

    # Flights 10 and above use label hierarchy. Change vote_weight parameter in
    # vote.py and MAKE SURE it matches the value in the corresponding comment

    # vote_weight = 0.9
    if flight == 100:
        cdsd_mips3 = pickle.load(open("pickles/cdsd_mips3_35170.pkl", 'rb'))
        print("# FLIGHT 10: yeast - MIPS3 - EC - baseline")
        folds = [2, 4, 6]
        graph_objs = [cdsd_mips3]
        voting_funcs = [vote.mv, vote.mv_hierarchy]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [1]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight100/"

    if flight == 101:
        cdsd_mips3 = pickle.load(open("pickles/cdsd_mips3_35170.pkl", 'rb'))
        print("# FLIGHT 10: yeast - MIPS3 - EC - cascade")
        folds = [2, 4, 6]
        graph_objs = [cdsd_mips3]
        voting_funcs = [vote.mv, vote.mv_hierarchy]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [12]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight101/"

    # vote_weight = 0.8
    if flight == 102:
        cdsd_mips3 = pickle.load(open("pickles/cdsd_mips3_35170.pkl", 'rb'))
        print("# FLIGHT 10: yeast - MIPS3 - EC - baseline")
        folds = [2, 4, 6]
        graph_objs = [cdsd_mips3]
        voting_funcs = [vote.mv_hierarchy]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [1]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight102/"

    if flight == 103:
        cdsd_mips3 = pickle.load(open("pickles/cdsd_mips3_35170.pkl", 'rb'))
        print("# FLIGHT 10: yeast - MIPS3 - EC - cascade")
        folds = [2, 4, 6]
        graph_objs = [cdsd_mips3]
        voting_funcs = [vote.mv_hierarchy]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [12]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight103/"

    # FLIGHT11 is weighted majority vote with hierarchy
    # vote_weight = 0.9
    if flight == 110:
        cdsd_mips3 = pickle.load(open("pickles/cdsd_mips3_35170.pkl", 'rb'))
        print("# FLIGHT 11: yeast - MIPS3 - EC - baseline")
        folds = [2, 4, 6]
        graph_objs = [cdsd_mips3]
        voting_funcs = [vote.wmv, vote.wmv_hierarchy]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [1]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight110/"

    if flight == 111:
        cdsd_mips3 = pickle.load(open("pickles/cdsd_mips3_35170.pkl", 'rb'))
        print("# FLIGHT 11: yeast - MIPS3 - EC - cascade")
        folds = [2, 4, 6]
        graph_objs = [cdsd_mips3]
        voting_funcs = [vote.wmv, vote.wmv_hierarchy]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [12]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight111/"

    #vote_weight = 0.8
    if flight == 112:
        cdsd_mips3 = pickle.load(open("pickles/cdsd_mips3_35170.pkl", 'rb'))
        print("# FLIGHT 11: yeast - MIPS3 - EC - baseline")
        folds = [2, 4, 6]
        graph_objs = [cdsd_mips3]
        voting_funcs = [vote.wmv_hierarchy]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [1]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight112/"

    if flight == 113:
        cdsd_mips3 = pickle.load(open("pickles/cdsd_mips3_35170.pkl", 'rb'))
        print("# FLIGHT 11: yeast - MIPS3 - EC - cascade")
        folds = [2, 4, 6]
        graph_objs = [cdsd_mips3]
        voting_funcs = [vote.wmv_hierarchy]
        conf_funcs = [conf.entropy_conf]
        conf_thresholds = [0.35]
        casc_rounds = [12]
        nb_types = ['known', 'all']
        OUTPUT_DIR = "raw_results/flight113/"

    # Run all combinations of voting_func, conf_funcs, conf_thresholds, for each graph type
    for graph in graph_objs:
        for vote in voting_funcs:
            for conf in conf_funcs:
                for thres in conf_thresholds:
                    for r in casc_rounds:
                        for fold in folds:
                            for nb_type in nb_types:
                                print(
                                    "Running acc test for: {} - {} - {} - {} - {} - {}r - {}f - {}"
                                    .format(
                                        graph.metric_type,
                                        graph.label_type,
                                        vote.__name__,
                                        conf.__name__,
                                        thres,
                                        r,
                                        fold,
                                        nb_type,
                                    ))
                                ofname = generate_filename(
                                    vote,
                                    conf,
                                    thres,
                                    graph.label_type,
                                    fold,
                                    nb_type,
                                    r,
                                    metric=graph.metric_type,
                                )
                                ofname = "{}{}".format(OUTPUT_DIR, ofname)

                                kwargs = {
                                    'ppigraph': graph,
                                    'cv_splits': fold,
                                    'labels': graph.label_type,
                                    'voting_func': vote,
                                    'conf_func': conf,
                                    'nb_type': nb_type,
                                    'conf_threshold': thres,
                                    'cascade_rounds': r,
                                }
                                kwargs = run_combo(**kwargs)
                                output_results(ofname, **kwargs)


if __name__ == "__main__":
    main(sys.argv)
