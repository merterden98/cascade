"""
PPIgraph.py

Base classes that model a PPI network, including PPINode and
 PPIGraph classes.

Each PPINode classes has a dictionary attribute that allows
for quick lookups of DSD or SP values to other nodes in the graph.
"""
import numpy as np


class PPINode(object):
    """
    Represents one node in a PPI network.

    Attributes:
        name (str): ORF identifier (e.g. 'YLR418C').
        dsd_dict (dict): Name, DSD value pairs to other nodes.
        sp_dict (dict): Name, shortest path value pairs to other nodes.
        labels (list): List of function labels.
        label_type (str): Type of function label (e.g. 'mips_1').
   
    Note:
        sorted_nodes_DSD and sorted_nodes_SP attributes contain list of
            other node names sorted by distance.
    """
    def __init__(self,
                 name=None,
                 dsd_dict=None,
                 sp_dict=None,
                 labels=None,
                 label_type=None,
                 hierarchy_labels=None):
        """
        Sets attributes.
        """
        self.name = name
        self.labels = labels
        self.label_type = label_type

        self.pseudo_label = None
        self.predicted_label = None
        self.label_conf = 0.0

        # Add hierarchical labels
        self.hierarchy_labels = hierarchy_labels
        self.graph = None

        # keep track of votes
        self.predicted_scores = {}

        # Distance dictionaries
        self.dsd_dict = dsd_dict

        # Sort other nodes in graph by DSD value
        self.sorted_nodes_DSD = self._get_sorted_nodes_DSD()

    def _get_sorted_nodes_DSD(self):
        """
        Returns list of all other node names sorted by DSD value.
        """
        if not self.dsd_dict:
            return None

        sorted_pairs = sorted(self.dsd_dict.items(), key=lambda x: x[1])

        # Only return node names
        return [pair[0] for pair in sorted_pairs]


class PPIGraph(object):
    """
    Represents entire PPI graph containing all PPINode objects.
    """
    def __init__(self, node_list=None, label_type=None, metric_type='DSD'):
        """
        Generate node dict and other inferred attributes.
        """
        self.node_list = np.array(node_list)

        # define training set
        # (nodes in node_list with a known annotation)
        self.training_nodes = [
            n for n in set(self.node_list) if n.labels != []
        ]

        self.label_type = label_type
        self.metric_type = metric_type

        # Set size of graph
        self.size = len(self.node_list)
        self.training_size = len(self.training_nodes)

        # Add parent Graph pointer to self on each node
        for n in node_list:
            n.graph = self

        # dictionary of label descendents.
        self.label_descendents = {}
        self.label_predecessors = {}
        self.generate_label_descendents()

    def generate_label_descendents(self):
        """
        Generate dictionary of label descendents based on set of labels
        in node_list.

        2019.7.17: hard-coded for mips level3
        """
        label_descendents = self.label_descendents
        label_predecessors = self.label_predecessors

        # Add all labels to label_descendents dict
        for node in self.node_list:
            node_hierarchy_labels = node.hierarchy_labels
            for labels_list in node_hierarchy_labels.values():
                for l in labels_list:
                    if l not in label_descendents:
                        label_descendents[l] = set()

        for node in self.node_list:
            if not node.labels: continue
            for l in node.labels:
                parts = l.split('.')
                if len(parts) != 3:
                    print('len violation')
                    continue
                l1 = parts[0]
                l2 = parts[0] + '.' + parts[1]
                label_descendents[l1].add(l2)
                label_descendents[l2].add(l)
                label_predecessors[l] = l2
                label_predecessors[l2] = l1

        for l, d in label_descendents.items():
            label_descendents[l] = list(d)
