import csv
from src import makegraph


# Hard code filenames - FLY
cdsd_fname = "flydata/biogrid35170.dmelanogaster.cdsd"
go_bp3_fname = "flydata/fly_associations_new.biological_process"
go_mf3_fname = "flydata/fly_associations_new.molecular_function"
outfile = "flydata/dmelanogaster_GO_inf.new.mfbp4"

mf3_fullgraph = makegraph.generate_graph_DSD(cdsd_fname,
                                             go_mf3_fname,
                                             "GO-mf3",
                                             metric_type="DSD")


# Keep labels with depth > ?
for node in mf3_fullgraph.node_list:
    deep_ls = [l for l in node.labels if int(l[-1]) == 4]
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

bp3_fullgraph = makegraph.generate_graph_DSD(cdsd_fname,
                                             go_bp3_fname,
                                             "GO-bp3",
                                             metric_type="DSD")

# Keep labels with depth > 3
for node in bp3_fullgraph.node_list:
    deep_ls = [l for l in node.labels if int(l[-1]) == 4]
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


# COMPUTE LABEL COVERAGE STATS
# load pickle
pfile = "pickles/fly.gomfbp4.dsd.pickle"
ppi_graph = pickle.load(open(pfile, 'rb'))

total_len = len(ppi_graph.node_list)
unlabeled_len = len(ppi_graph.unlabelled_nodes)
print(total_len)
print(unlabeled_len)

total_labels = 0
for node in ppi_graph.node_list:
    total_labels += len(node.labels)
    
print(total_labels)
