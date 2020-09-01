# gaf_to_func.fly.py
import csv
from collections import defaultdict

fname = "sampledata/fb.gaf.clean"

with open(fname, "r") as f:
    reader = csv.reader(f, delimiter="\t")
    raw_data = list(reader)

    
r = raw_data[11]
for i, val in enumerate(r):
    print("{} \t {}".format(i, val))



