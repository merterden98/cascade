# yeast_mips3_cv.sh
#
# Description:
# Script for running baseline CV on hierarchical methods
# for yeast PPI using MIPS 3 labels

# ALL tests should use following cascade settings:
# conftype = ENT
# cascade rounds = 12
# threshold = 0.35

# Compare using MV:
# a) cascade all
# b) cascade known
# c) cascade all_hierarchical

# SET RESULTS OUTPUT DIR
RESULTS=july02_results/

# -------------------------------------------------------
#                  MIPS 3 - 2fold cv                    #

# mips3 - 2fold - mv all ;
# python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
#         --type=PICKLE \
#         --vtype=MV \
#         --conftype=ENT \
#         --threshold=0.35 \
#         --ntype=all \
#         --rounds=12 \
#         --cv_rounds=2 \
#         --mode=cv \
#         --outdir=$RESULTS

# # mips3 - 2fold - mv known ;
# python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
#         --type=PICKLE \
#         --vtype=MV \
#         --conftype=ENT \
#         --threshold=0.35 \
#         --ntype=known \
#         --rounds=12 \
#         --cv_rounds=2 \
#         --mode=cv \
#         --outdir=$RESULTS

# mips3 - 2fold - mvh allh ;
python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
        --type=PICKLE \
        --vtype=MVH \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all_h \
        --rounds=12 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=$RESULTS

# -------------------------------------------------------
#                  MIPS 3 - 4fold cv                    #

# mips3 - 4fold - mv all ;
# python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
#         --type=PICKLE \
#         --vtype=MV \
#         --conftype=ENT \
#         --threshold=0.35 \
#         --ntype=all \
#         --rounds=12 \
#         --cv_rounds=4 \
#         --mode=cv \
#         --outdir=$RESULTS

# # mips3 - 4fold - mv known ;
# python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
#         --type=PICKLE \
#         --vtype=MV \
#         --conftype=ENT \
#         --threshold=0.35 \
#         --ntype=known \
#         --rounds=12 \
#         --cv_rounds=4 \
#         --mode=cv \
#         --outdir=$RESULTS

# mips3 - 4fold - mvh allh ;
python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
        --type=PICKLE \
        --vtype=MVH \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all_h \
        --rounds=12 \
        --cv_rounds=4 \
        --mode=cv \
        --outdir=$RESULTS


# -------------------------------------------------------
#                  MIPS 3 - 6fold cv                    #

# mips3 - 6fold - mv all ;
# python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
#         --type=PICKLE \
#         --vtype=MV \
#         --conftype=ENT \
#         --threshold=0.35 \
#         --ntype=all \
#         --rounds=12 \
#         --cv_rounds=6 \
#         --mode=cv \
#         --outdir=$RESULTS

# mips3 - 6fold - mv known ;
# python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
#         --type=PICKLE \
#         --vtype=MV \
#         --conftype=ENT \
#         --threshold=0.35 \
#         --ntype=known \
#         --rounds=12 \
#         --cv_rounds=6 \
#         --mode=cv \
#         --outdir=$RESULTS

# mips3 - 6fold - mvh allh ;
python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
        --type=PICKLE \
        --vtype=MVH \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all_h \
        --rounds=12 \
        --cv_rounds=6 \
        --mode=cv \
        --outdir=$RESULTS
