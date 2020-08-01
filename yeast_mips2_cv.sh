# yeast_mips2_cv.sh
#
# Description:
# Script for running baseline CV on hierarchical methods
# for yeast PPI using MIPS 2 labels

# ALL tests should use following cascade settings:
# conftype = ENT
# cascade rounds = 12
# threshold = 0.35

# Compare using MV:
# a) cascade all
# b) cascade known
# c) cascade all_hierarchical

# SET RESULTS OUTPUT DIR
RESULTS=aug01_results/

# -------------------------------------------------------
#                  MIPS 2 - 2fold cv                    #

# mips2 - 2fold - mv all ;
python3 run.py --infile=pickles/yeast.mips2.dsd.pickle \
        --type=PICKLE \
        --vtype=MV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all \
        --rounds=12 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=$RESULTS

# mips2 - 2fold - mv known ;
python3 run.py --infile=pickles/yeast.mips2.dsd.pickle \
        --type=PICKLE \
        --vtype=MV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=known \
        --rounds=12 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=$RESULTS

# mips2 - 2fold - mvh allh ;
python3 run.py --infile=pickles/yeast.mips2.dsd.pickle \
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
#                  MIPS 2 - 4fold cv                    #

# mips2 - 4fold - mv all ;
python3 run.py --infile=pickles/yeast.mips2.dsd.pickle \
        --type=PICKLE \
        --vtype=MV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all \
        --rounds=12 \
        --cv_rounds=4 \
        --mode=cv \
        --outdir=$RESULTS

# mips2 - 4fold - mv known ;
python3 run.py --infile=pickles/yeast.mips2.dsd.pickle \
        --type=PICKLE \
        --vtype=MV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=known \
        --rounds=12 \
        --cv_rounds=4 \
        --mode=cv \
        --outdir=$RESULTS

# mips2 - 4fold - mvh allh ;
python3 run.py --infile=pickles/yeast.mips2.dsd.pickle \
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
#                  MIPS 2 - 6fold cv                    #

# mips2 - 6fold - mv all ;
python3 run.py --infile=pickles/yeast.mips2.dsd.pickle \
        --type=PICKLE \
        --vtype=MV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all \
        --rounds=12 \
        --cv_rounds=6 \
        --mode=cv \
        --outdir=$RESULTS

# mips2 - 6fold - mv known ;
python3 run.py --infile=pickles/yeast.mips2.dsd.pickle \
        --type=PICKLE \
        --vtype=MV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=known \
        --rounds=12 \
        --cv_rounds=6 \
        --mode=cv \
        --outdir=$RESULTS

# mips2 - 6fold - mvh allh ;
python3 run.py --infile=pickles/yeast.mips2.dsd.pickle \
        --type=PICKLE \
        --vtype=MVH \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all_h \
        --rounds=12 \
        --cv_rounds=6 \
        --mode=cv \
        --outdir=$RESULTS
