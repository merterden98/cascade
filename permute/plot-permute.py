# plot-permute.py
#
# JML, January 2021
import numpy as np
import pickle
import  matplotlib.pyplot as plt

confs_pfile = "confs_vals.pickle"
confs = pickle.load(open(confs_pfile, "rb"))
runs = 50

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 12))

fig.suptitle(
    "Confidence Score Distribution for Correct Predictions\n" +
    "S. cerevisiae with Randomly-Permuted GO-MFBP4 Label Sets " +
    "({} runs, {} total points)\n".format(runs, len(confs)) + 
    "Cascade Settings: 2-fold, cDSD-WMV-Known, CC conf, " +
    "12 rounds, 35% thresh.",
)


ax1.set_title("Histogram")
ax1.set_ylabel("Count")
ax1.set_xlabel("Confidence Score")
ax1.hist(confs, bins=100, color="blue", rwidth=0.99)

ax2.set_title("Density")
ax2.set_xlabel("Confidence Score")
ax2.hist(confs, density=True, bins=100, color="blue", rwidth=0.99)

print("conf label size = {}".format(len(confs)))
print("conf mean = {}".format(np.mean(confs)))
print("conf std = {}\n".format(np.std(confs)))


plt.tight_layout(rect=[0, 0, 1, 0.9])
plt.subplots_adjust(hspace=0.23)
plt.show()

