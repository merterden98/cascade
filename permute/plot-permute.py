# plot-permute.py
#
# JML, January 2021
import numpy as np
import pickle
import  matplotlib.pyplot as plt

yeast_confs_pfile = "confs_vals_yeast.pickle"
fly_confs_pfile = "confs_vals_fly.pickle"
yeast_confs = pickle.load(open(yeast_confs_pfile, "rb"))
fly_confs = pickle.load(open(fly_confs_pfile, "rb"))
runs = 50

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), dpi=150)

fig.suptitle(
    "Confidence Score Histograms -- Random Permutation Tests\n" +    
    "(2-Fold, 12 cascade rounds; cDSD-WMV-Known, CC, 35% threshold)",
    weight="bold",
    size=14,
)


ax1.set_title(
    "Yeast - GOMFBP4 - (50 permutations, {} scores)".format(len(yeast_confs)),
    size=12,
    weight="bold",
)
ax1.set_xlabel("Confidence Score")
ax1.set_ylabel("Count")
ax1.hist(yeast_confs, bins=100, color="blue", rwidth=1.0)

ax2.set_title(
    "Fly - GOMFBP4 - (50 permutations, {} scores)".format(len(fly_confs)),
    size=12,
    weight="bold"
)
ax2.set_xlabel("Confidence Score")
ax2.set_ylabel("Count")
ax2.hist(fly_confs, bins=100, color="blue", rwidth=1.0)

print("yeast - conf label size = {}".format(len(yeast_confs)))
print("yeast - conf mean = {}".format(np.mean(yeast_confs)))
print("yeast - conf std = {}\n".format(np.std(yeast_confs)))

print("fly - conf label size = {}".format(len(fly_confs)))
print("fly - conf mean = {}".format(np.mean(fly_confs)))
print("fly - conf std = {}\n".format(np.std(fly_confs)))


plt.tight_layout(rect=[0, 0, 1, 0.9])
plt.subplots_adjust(hspace=0.3)
plt.savefig("permute.histogram.overall.v3.png")

