# yeast_mips3_h_cv.wmv.sh
#
# Description:
# Script for running CV on hierarchical methods
# for yeast PPI using MIPS 3 labels

# WMV version -- cascade all_hierarchical

# ALL tests should use following cascade settings:
# conftype = ENT
# cascade rounds = 12
# threshold = 0.35

# SET RESULTS OUTPUT DIR
RESULTS=aug_results/

# -------------------------------------------------------
#                  MIPS 3 - 2fold cv                    #

# mips3 - 2fold - wmvh allh ;
python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
        --type=PICKLE \
        --vtype=WMVH \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all_h \
        --rounds=12 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=$RESULTS

# -------------------------------------------------------
#                  MIPS 3 - 4fold cv                    #

# mips3 - 4fold - wmvh allh ;
python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
        --type=PICKLE \
        --vtype=WMVH \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all_h \
        --rounds=12 \
        --cv_rounds=4 \
        --mode=cv \
        --outdir=$RESULTS


# -------------------------------------------------------
#                  MIPS 3 - 6fold cv                    #

# mips3 - 6fold - wmvh allh ;
python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
        --type=PICKLE \
        --vtype=WMVH \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all_h \
        --rounds=12 \
        --cv_rounds=6 \
        --mode=cv \
        --outdir=$RESULTS
