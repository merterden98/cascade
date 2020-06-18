from src import makegraph
from src import crossvalidate

API = {
    "getPPIGraph": makegraph.getPPIGraph,
    "runCV": crossvalidate.run_kfold_cv
}

'''
    getPPIGraph: 
    :param str matrix_filename: filepath to matrix containing edge-data i,e DSD/cDSD
    :param str labels_filename: file that contains label metadata see MIPSFirstLabels.list
    :param str label_type: Specifier to indicate if we use GO or MIPS labels
    :param bool heirarychy_labels: If labels have heirarchy, get heirarchy metadata
    :param str metric_type: What kind of edge metric are we using. *Note if DSD specified
                            we use a prebuilt custom_node_list_generator.
    :param (str, {str: [str]}) -> [[str, {str: float]] custom_node_list_generator:
           A function that takes matrix_filename, and a dictionary that maps a node
           name to a set of labels, and returns an array where each element is an
           array such that the first element is the name of the node, and the second
           is a dictionary that maps neighbors with the associated edge value. 
           See ./src/makegraph.py#load_dsd_matrix for example.
    
    :returns a PPIGraph Object
'''
getPPIGraph = API["getPPIGraph"]


# voteFuncType: (node, [str (of node names)], {node: [labels}) -> str (prediction)
# confFuncType: (node, [str (of node names)], {node: [labels}) -> float (confidence)

'''
    runCV: *Note runs 10 Round
    :param PPIGraph ppigraph: A graph object the contains network data
    :param int cv_splits: Number of splits we want in our Cross Validation
    :param voteFuncType voting_func: See above for type hint, a function that
                                      assigns a label for a node based on its neighbors.
    :param confFuncType conf_func: See above for type hint, function that assigns confidence
                                   value.
    :param int K: number of neighbors
    :param int cascade_rounds: number of times to run cascade procedure.
    :param float conf_threshold: minimum cut-off value for confidence values in predictions.
    returns: [[accuracy], [f1 scores]], an array containing accuracy of predictions, and
                                        f1 scores.
'''
runCV = API["runCV"]























'''BELOW THIS IS FOR KAPIL TO SEE'''

import pprint
import json
import numpy as np

def get_kapil_node_list(matrix_file, nodelist):
    labels_dict = makegraph.load_labels('./data/MIPSFirstLevel.list')
    with open('node_dict_reduced.json', 'r') as f:
        adj_dict = json.load(f)
    
    full_node_list = []
    ray = np.load(matrix_file)
    for i, row in enumerate(ray):
        vals_dict = {}
        for j, val in enumerate(row):
            other_node = adj_dict[str(j)]
            if other_node in labels_dict:
                if not labels_dict[other_node]:
                    continue
                vals_dict[other_node] = float(val)
            pprint.pprint(vals_dict)
        full_node_list.append([adj_dict[str(i)], vals_dict])
    
    return full_node_list
    
