# load 3+, 4+ into sets

from collections import defaultdict
import json
go_level_3 = set()
with open("sampledata/fly_associations_bpmf_level_3.txt") as f:
    for line in f:
        row = line.split()
        if len(row) > 1:
            for item in row[1:]:
                go_level_3.add(item)

go_level_4 = set()
with open("sampledata/fly_associations_bpmf_level_4.txt") as f:
    for line in f:
        row = line.split()
        if len(row) > 1:
            for item in row[1:]:
                go_level_4.add(item)

go_level_5 = set()
with open("sampledata/fly_associations_bpmf_level_5.txt") as f:
    for line in f:
        row = line.split()
        if len(row) > 1:
            for item in row[1:]:
                go_level_5.add(item)

go_level_6 = set()
with open("sampledata/fly_associations_bpmf_level_6.txt") as f:
    for line in f:
        row = line.split()
        if len(row) > 1:
            for item in row[1:]:
                go_level_6.add(item)

level_4_only = go_level_4.difference(go_level_5)
level_3_only = go_level_3.difference(go_level_4)
level_5_only = go_level_5.difference(go_level_6)

with open("sampledata/flybase_to_annotation_ids.json") as f:
    fb_dict = json.load(f)

fb_dict = {v: k for k, v in fb_dict.items()}

protein_to_go = {}
with open("sampledata/fly_associations_bpmf_level_4.txt") as f:
    for line in f:
        row = line.split()
        if row[0] in fb_dict:
            if len(row) > 1:
                protein_to_go[fb_dict[row[0]]] = [
                    f"{label}@4" for label in row[1:] if label in level_4_only]
            else:
                protein_to_go[fb_dict[row[0]]] = []


freq_dict = defaultdict(int)

for key, value in protein_to_go.items():
    for label in value:
        freq_dict[label] += 1

filtered_labels = dict()

for key, value in protein_to_go.items():
    filtered_labels[key] = [label for label in value if freq_dict[label] > 50]

for _, cg in fb_dict.items():
    if cg not in filtered_labels:
        filtered_labels[cg] = []
