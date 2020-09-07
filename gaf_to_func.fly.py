# gaf_to_func.fly.py
import csv
from collections import defaultdict

# SUPPORT = ["EXP", "IMP", "ISS", "ISM", "TAS", "IEA", "HMP", "IDA", "IGI",
#            "ISO", "IGC", "NAS", "HGI", "IPI", "IEP", "ISA", "RCA", "IC", "HDA"]

SUPPORT = ["EXP", "IMP", "HMP", "HEP", "IDA", "IGI", "HGI", "IPI", "IEP", "HDA"]

ANNOTATION_TYPES = ["P", "F", "C"]  # Use C for Cellular comp.



def write_preamble(f):
    support = " ".join(SUPPORT)
    f.write("# species: Drosophila melanogaster\n")
    f.write(f"# support: {support}\n")
    for _ in range(18):
        f.write("# \n")


def go_compare(x):
    go_label = x[0]
    go_val = int(go_label[3:])
    return go_val


fname = "sampledata/fb.gaf.clean"

with open(fname, "r") as f:
    reader = csv.reader(f, delimiter="\t")
    raw_data = list(reader)

func_to_go = defaultdict(list)

for row in raw_data:
    go_label = row[4]
    exp_type = row[6]
    go_type = row[8]
    id_list = row[10].split("|")
    
    for i, item in enumerate(id_list):
        if item.startswith("CG"):
            func_to_go[id_list[i]] += [(go_label, exp_type, go_type)]
            continue
        # print("no CG")

go_to_gene = defaultdict(list)

for key, vals in func_to_go.items():
   for go_label, exp_type, go_type in vals:
        if exp_type in SUPPORT and go_type in ANNOTATION_TYPES:
            go_to_gene[go_label] += [key]

go_to_gene_list = sorted(list(go_to_gene.items()), key=go_compare)
with open(f"{fname}.associations.2", "w") as f:
    write_preamble(f)
    for go_label, protein_list in go_to_gene_list:
        protein_str = " ".join(protein_list)
        f.write(f"{go_label}\tPROTEIN_FUNCTIONALITY\t{protein_str}\n")
