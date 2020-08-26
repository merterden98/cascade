"""
makegraph.py

Module used for generating graph object from PPI and function label data.

"""
import json
import csv
import numpy as np
import pprint
from . import graph
from functools import reduce


def load_labels(labels_fname):
    """
    Load file of function labels and formats data into dictionary of 
    node name, labels list pairs.

    File expected to be tab or space delimited.
    """
    with open(labels_fname, 'r') as f:
        data = [row.strip() for row in f.readlines()]

    labels_dict = {}

    for row in data:
        row_string = row.split(' ')
        row_parts = [s for s in row_string if s is not '']
        name = row_parts[0]
        labels = [l for l in row_parts[1:] if l is not '#']
        labels_dict[name] = labels

    return labels_dict


def load_GOlabels(labels_fname):
    """
    Same as load_labels function, but formatted for GO annotation file

    Tab-delimited
    """

    print("loading GO labels")

    with open(labels_fname, 'r') as f:
        data = [row.strip() for row in f.readlines()]

    labels_dict = {}

    for row in data:
        row_parts = row.split('\t')
        name = row_parts[0]
        labels = row_parts[1:]
        labels_dict[name] = labels
    return labels_dict


def mips_from_length(label_list):
    if not label_list:
        return "UNKNOWN"
    else:
        if len(label_list[0]) == 2:
            return "1"
        elif len(label_list[0]) == 5:
            return "2"
        elif len(label_list[0]) == 8:
            return "3"
    return "UNKNOWN"


def merge_hierarchy_labels(hierarchy_labels_dict_list):

    for label_dict in hierarchy_labels_dict_list:
        for protein_name in label_dict.keys():
            # Creates  [(MIPS_LEVEL, LABEL_LIST)] for every protein
            label_dict[protein_name] = [
                (mips_from_length(label_dict[protein_name]),
                 label_dict[protein_name])
            ]

    def merge(accum, new_dict):
        if not accum:
            return new_dict
        else:
            for key in accum.keys():
                if key in new_dict:
                    prev = accum[key]
                    accum[key] = prev + new_dict[key]
            return accum

    a = reduce(merge, hierarchy_labels_dict_list, {})
    return a


def load_dsd_matrix(dsd_fname, labels_dict):
    """
    Load DSD matrix and generate graph as an adjacency list. 
    Each node owns a dictionary of other node names, dsd value pairs.

    Only nodes with known labels from the labels_dict are added to 
    the graph.

    Returns an array of lists containing [node name, dsd values dict]
    for each node, where dsd value dict contains 
    {'other node name': dsd value} pairs.
    """
    with open(dsd_fname, 'r') as f:
        csv_reader = csv.reader(f, delimiter='\t')
        data = [row for row in csv_reader]

    full_node_list = []

    # Split DSD data into headers and rows
    headers = data[0][1:]
    rows = data[1:]

    # Extract name and DSD values for each node
    for i, row in enumerate(rows):

        # Unpack row
        name = row[0]
        dsd_list = row[1:]

        # Prepare dict of DSD values for given node
        # Add every other node, value pair (converted to float)
        # Only add node if label is known and has non empty labels list
        vals_dict = {}
        for j, val in enumerate(dsd_list):
            other_node = headers[j]

            if other_node in labels_dict:
                if not labels_dict[other_node]:
                    continue
                vals_dict[other_node] = float(val)

        full_node_list.append([name, vals_dict])

    return full_node_list


def format_nodes_DSD(node_list=None,
                     labels_dict=None,
                     label_type=None,
                     hierarchy_labels_dict=None):
    """
    Maps nodes with DSD values and corresponding function labels 
        into set of PPINode objects.

    Args:
        node_list (list): List of nodes and corresponding DSD dicts.
        labels_dict (dict): Node, function label pairs.
        label_type (str): Type of function label (e.g. 'mips_1').

    Returns:
        List of `PPINode` objects.
    """

    # Map nodes from DSD matrix with function labels in labels_dict
    new_graph = []

    for n in node_list:

        # Unpack rows in node_list
        name = n[0]
        dsd_vals_dict = n[1]

        # Get corresponding function labels
        try:
            node_labels = labels_dict[name]
        except KeyError:
            node_labels = []

        hierarchy_labels = []
        if name in hierarchy_labels_dict:
            hierarchy_labels = hierarchy_labels_dict[name]
        # Create PPINode object
        node_obj = graph.PPINode(name=name,
                                 dsd_dict=dsd_vals_dict,
                                 labels=node_labels,
                                 label_type=label_type,
                                 hierarchy_labels=hierarchy_labels)

        new_graph.append(node_obj)

    return new_graph


def generate_graph_DSD(dsd_filename,
                       labels_filename,
                       label_type,
                       hierarchy_labels_dict=None,
                       metric_type='DSD'):
    """
    Generates PPIGraph object containing PPINodes for graphs using
    DSD metric values.
    """
    # Load and format function labels
    print("Loading labels file")
    if 'GO' in label_type:
        labels_dict = load_GOlabels(labels_filename)
    else:
        labels_dict = load_labels(labels_filename)

    if metric_type == 'DSD':
        # Load DSD matrix and format list of nodes
        print("Loading DSD file and preparing DSD dicts")
        node_list = load_dsd_matrix(dsd_filename, labels_dict)

    # Create PPINode objects
    print("Formatting PPINodes")
    ppi_nodes = format_nodes_DSD(node_list=node_list,
                                 labels_dict=labels_dict,
                                 label_type=label_type,
                                 hierarchy_labels_dict=hierarchy_labels_dict)
    # Create PPIGraph object
    print("Creating new PPIGraph")
    new_PPIGraph = graph.PPIGraph(node_list=ppi_nodes,
                                  label_type=label_type,
                                  metric_type=metric_type)

    return new_PPIGraph


def getPPIGraph(matrix_filename, labels_filename, label_type, metric_type,
                hierarchy_files):

    hierarchy_labels_dict_list = []
    merged_hierarchy_labels_dict = {}
    if hierarchy_files:
        hierarchy_labels_dict_list = [
            load_labels(hfile) for hfile in hierarchy_files
        ]
        merged_hierarchy_labels_dict = merge_hierarchy_labels(
            hierarchy_labels_dict_list)

    return generate_graph_DSD(
        dsd_filename=matrix_filename,
        labels_filename=labels_filename,
        label_type=label_type,
        metric_type=metric_type,
        hierarchy_labels_dict=merged_hierarchy_labels_dict)
