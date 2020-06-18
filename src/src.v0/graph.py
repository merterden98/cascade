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
    def __init__(self, name=None, dsd_dict=None, 
                 sp_dict=None, labels=None,
                 label_type=None):
        """
        Sets attributes.
        """
        self.name = name
        self.labels = labels
        self.label_type = label_type

        self.pseudo_label = None
        self.predicted_label = None
        
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

    def _get_sorted_nodes_SP(self):
        """
        Returns a list of all other node names sorted by SP distance.
        """
        if not self.sp_dict:
            return None
        
        sorted_pairs = sorted(self.sp_dict.items(), key=lambda x: x[1])

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
        self.label_type = label_type
        self.metric_type = metric_type
        
        # Set size of graph
        self.size = len(self.node_list)
        
