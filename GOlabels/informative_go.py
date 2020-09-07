#!/usr/bin/env python

# informative_go.py
# by John Lazarsfeld, Jonathan Rodriguez, and Mert Erden
# March 22, 2019

# Extract informative GO terms from full GO label set.
# Informative terms are those that are:
#    - at least 3 levels below the root
#    - annotate more than 50 proteins in the dataset
#    - see Cao 2013 (and Deng 2003)

# General strategy:
# - load full dataset into PPIGraph
# - in each node, remove labels less than 3 levels below root (@0, @1, @2)
# - begin working dictionary of labels, annotation count
# - filter labels with > 50 annotations
# - in each node, only keep labels with > 50 annotations
# - print list of informative terms
# - print tsv with updated GO terms

import csv
from src import makegraph

# Hard code filenames - YEAST
cdsd_fname = "data/biogrid35170.scerevisiae.cdsd"
go_bp3_fname = "data/scerevisiae_systematic_associations.biological_process"
go_mf3_fname = "data/scerevisiae_systematic_associations.molecular_function"
outfile = "scerevisiae_GO_inf_level6.mfbp3"

# Hard code filenames - FLY
# cdsd_fname = "data/biogrid35170.dmelanogaster.cdsd"
# go_bp3_fname = "data/dmelanogaster_systematic_associations.biological_process"
# go_mf3_fname = "data/dmelanogaster_systematic_associations.molecular_function"
# outfile = "dmelanogaster_GO_inf_level6.mfbp3"


# ---------------------------------------------------------------------------
#                             MOLECULAR FUNCTION
#

mf3_fullgraph = makegraph.generate_graph_DSD(dsd_filename=cdsd_fname,
                                             labels_filename=go_mf3_fname,
                                             label_type="GO-mf3",
                                             metric_type="CDSD")

# Keep labels with depth > ?
for node in mf3_fullgraph.node_list:
    deep_ls = [l for l in node.labels if int(l[-1]) == 6]
    node.labels = deep_ls

# Generate annotation frequency for remaining labels
ls_dict = {}
for node in mf3_fullgraph.node_list:
    for l in node.labels:
        if l in ls_dict:
            ls_dict[l] += 1
        else:
            ls_dict[l] = 1

# Filter labels with > 50 annotations in set
ls_highfreq_set = set()
for l, freq in ls_dict.items():
    if freq > 50:
        ls_highfreq_set.add(l)
print("Molecular Function: {} informative nodes".format(len(ls_highfreq_set)))

for node in mf3_fullgraph.node_list:
    updated_labels = [l for l in node.labels if l in ls_highfreq_set]
    node.labels = updated_labels


# ---------------------------------------------------------------------------
#                             BIOLOGICAL PROCESS
#

bp3_fullgraph = makegraph.generate_graph_DSD(dsd_filename=cdsd_fname,
                                             labels_filename=go_bp3_fname,
                                             label_type="GO-bp3",
                                             metric_type="CDSD")

# Keep labels with depth > 3
for node in bp3_fullgraph.node_list:
    deep_ls = [l for l in node.labels if int(l[-1]) == 6]
    node.labels = deep_ls

# Generate annotation frequency for remaining labels
bls_dict = {}
for node in bp3_fullgraph.node_list:
    for l in node.labels:
        if l in bls_dict:
            bls_dict[l] += 1
        else:
            bls_dict[l] = 1

# Filter labels with > 50 annotations in set
bls_highfreq_set = set()
for l, freq in bls_dict.items():
    if freq > 50:
        bls_highfreq_set.add(l)
print("Biological Process: {} informative nodes".format(len(bls_highfreq_set)))
        
for node in bp3_fullgraph.node_list:
    updated_labels = [l for l in node.labels if l in bls_highfreq_set]
    node.labels = updated_labels

# MERGE BP an MF

union_dict = {}
for node in mf3_fullgraph.node_list:
    if node.name not in union_dict: union_dict[node.name] = set()
    for l in node.labels:
        union_dict[node.name].add(l)

for node in bp3_fullgraph.node_list:
    if node.name not in union_dict: union_dict[node.name] = set()
    for l in node.labels:
        union_dict[node.name].add(l)

mfbp3_label_rows = []
for key, val in union_dict.items():
    row = []
    row.append(key)
    labels = list(val)
    for l in labels:
        row.append(l)
    mfbp3_label_rows.append(row)

with open(outfile, 'w') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(mfbp3_label_rows)



#---------------------------------------------------------------------------
# OLD:
    
#---------------------------------------------------------------------------
#                            WRITE MOLECULAR FUNCTION
           
# #write updated labels to file
# mf3_label_rows = []
# for node in mf3_fullgraph.node_list:
#     row = []
#     row.append(node.name)
#     for l in node.labels:
#         row.append(l)
#     mf3_label_rows.append(row)

# with open("data/scerevisiae_GO_full.mf3", 'w') as f:
#     writer = csv.writer(f, delimiter='\t')
#     writer.writerows(mf3_label_rows)


# ---------------------------------------------------------------------------
#                             BIOLOGICAL PROCESS
#

# bp3_fullgraph = makegraph.generate_graph_DSD(dsd_filename=cdsd_fname,
#                                              labels_filename=go_bp3_fname,
#                                              label_type="GO-bp3",
#                                              metric_type="CDSD")

# # Keep labels with depth > 3
# for node in bp3_fullgraph.node_list:
#     deep_ls = [l for l in node.labels if int(l[-1]) > 3]
#     node.labels = deep_ls

    
# # ---------------------------------------------------------------------------
# #                             BIOLOGICAL PROCESS - 
# #

# # Generate annotation frequency for remaining labels
# ls_dict = {}
# for node in bp3_fullgraph.node_list:
#     for l in node.labels:
#         if l in ls_dict:
#             ls_dict[l] += 1
#         else:
#             ls_dict[l] = 1


# # Filter labels with > 50 annotations in set
# ls_highfreq_set = set()
# for l, freq in ls_dict.items():
#     if freq > 50:
#         ls_highfreq_set.add(l)

# Write informative GO terms to file
# ls_highfreq = list(ls_highfreq_set)
# ls_highfreq_sorted = sorted([(l, ls_dict[l]) for l in ls_highfreq], key=lambda x: x[1], reverse=True)

# with open("informative_go_terms.txt", 'w') as f:
#     for r in ls_highfreq_sorted:
#         f.write("{}\t{}\n".format(r[0], r[1]))
        
                
# #Update labels on nodes to only include those in ls_highfreq_set
# for node in bp3_fullgraph.node_list:
#     updated_labels = [l for l in node.labels if l in ls_highfreq_set]
#     node.labels = updated_labels

# compute / print stats
# num_highfreq_labels = len(ls_highfreq_set)
# num_total_nodes = len(bp3_fullgraph.node_list)
# num_labeled_nodes = len([n for n in bp3_fullgraph.node_list if n.labels != []])

# print("Number informative labels: {}".format(num_highfreq_labels))
# print("Number labeled nodes: {} / {}".format(num_labeled_nodes, num_total_nodes))


# ---------------------------------------------------------------------------
#                             WRITE BIOLOGICAL PROCESS 
#

# write updated labels to file
# bp3_label_rows = []
# for node in bp3_fullgraph.node_list:
#     row = []
#     row.append(node.name)
#     for l in node.labels:
#         row.append(l)
#     bp3_label_rows.append(row)

# with open(outfile, 'w') as f:
#     writer = csv.writer(f, delimiter='\t')
#     writer.writerows(bp3_label_rows)    

    

# ---------------------------------------------------------------------------
#                             MOLECULAR FUNCTION
#

# mf3_fullgraph = makegraph.generate_graph_DSD(dsd_filename=cdsd_fname,
#                                              labels_filename=go_mf3_fname,
#                                              label_type="GO-mf3",
#                                              metric_type="CDSD")

# # Keep labels with depth > 3
# for node in mf3_fullgraph.node_list:
#     deep_ls = [l for l in node.labels if int(l[-1]) > 3]
#     node.labels = deep_ls
    
# ---------------------------------------------------------------------------
#                             WRITE MOLECULAR FUNCTION
#            


# write updated labels to file
# mf3_label_rows = []
# for node in mf3_fullgraph.node_list:
#     row = []
#     row.append(node.name)
#     for l in node.labels:
#         row.append(l)
#     mf3_label_rows.append(row)

# with open("data/scerevisiae_GO_full.mf3", 'w') as f:
#     writer = csv.writer(f, delimiter='\t')
#     writer.writerows(mf3_label_rows)

