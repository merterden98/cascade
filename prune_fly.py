from collections import defaultdict
import json
import sys
import pprint

with open("sampledata/flybase_to_annotation_ids.json") as f:
    fb_dict = json.load(f)

fb_dict = {v: k for k, v in fb_dict.items()}


id_to_go = dict()
with open(sys.argv[1]) as f:
    for line in f:
        row = line.split()
        if row[0] in fb_dict:
            id_to_go[fb_dict[row[0]]] = row[1:]


freq = defaultdict(int)
for _, vals in id_to_go.items():
    for val in vals:
        freq[val] += 1

greater_than_50_proteins = [key for key, val in freq.items() if val >= 50]

pruned_annotations = {key: [
    val for val in vals if val in greater_than_50_proteins] for key, vals in id_to_go.items()}


with open(f"{sys.argv[1]}.pruned", "w") as f:
    for protein, labels in pruned_annotations.items():
        tab_delimited_labels = '\t'.join(labels) if len(labels) > 0 else ''
        if tab_delimited_labels == '':
            f.write(f"{protein}{tab_delimited_labels}\n")
        else:
            f.write(f"{protein}\t{tab_delimited_labels}\n")
