# yeast_mips2_cv.wmv.sh
#
# Description:
# Script for running baseline CV on hierarchical methods
# for yeast PPI using MIPS 2 labels

# WMV baseline (don't do hierarchical method here)

# ALL tests should use following cascade settings:
# conftype = ENT
# cascade rounds = 12
# threshold = 0.35

# Compare using WMV:
# a) cascade all
# b) cascade known
# c) cascade all_hierarchical

# SET RESULTS OUTPUT DIR
RESULTS=aug_results/

# -------------------------------------------------------
#                  MIPS 2 - 2fold cv                    #

# mips2 - 2fold - wmv all ;
python3 run.py --infile=pickles/yeast.mips2.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all \
        --rounds=12 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=$RESULTS

# mips2 - 2fold - wmv known ;
python3 run.py --infile=pickles/yeast.mips2.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=known \
        --rounds=12 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=$RESULTS

# -------------------------------------------------------
#                  MIPS 2 - 4fold cv                    #

# mips2 - 4fold - wmv all ;
python3 run.py --infile=pickles/yeast.mips2.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all \
        --rounds=12 \
        --cv_rounds=4 \
        --mode=cv \
        --outdir=$RESULTS

# mips2 - 4fold - wmv known ;
python3 run.py --infile=pickles/yeast.mips2.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=known \
        --rounds=12 \
        --cv_rounds=4 \
        --mode=cv \
        --outdir=$RESULTS


# -------------------------------------------------------
#                  MIPS 2 - 6fold cv                    #

# mips2 - 6fold - wmv all ;
python3 run.py --infile=pickles/yeast.mips2.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all \
        --rounds=12 \
        --cv_rounds=6 \
        --mode=cv \
        --outdir=$RESULTS

# mips2 - 6fold - wmv known ;
python3 run.py --infile=pickles/yeast.mips2.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=known \
        --rounds=12 \
        --cv_rounds=6 \
        --mode=cv \
        --outdir=$RESULTS


# -------------------------------------------------------
#                  MIPS 3 - 2fold cv                    #

# mips3 - 2fold - wmv all ;
python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all \
        --rounds=12 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=$RESULTS

# mips3 - 2fold - wmv known ;
python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=known \
        --rounds=12 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=$RESULTS

# -------------------------------------------------------
#                  MIPS 2 - 4fold cv                    #

# mips3 - 4fold - wmv all ;
python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all \
        --rounds=12 \
        --cv_rounds=4 \
        --mode=cv \
        --outdir=$RESULTS

# mips3 - 4fold - wmv known ;
python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=known \
        --rounds=12 \
        --cv_rounds=4 \
        --mode=cv \
        --outdir=$RESULTS


# -------------------------------------------------------
#                  MIPS 2 - 6fold cv                    #

# mips3 - 6fold - wmv all ;
python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all \
        --rounds=12 \
        --cv_rounds=6 \
        --mode=cv \
        --outdir=$RESULTS

# mips3 - 6fold - wmv known ;
python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=known \
        --rounds=12 \
        --cv_rounds=6 \
        --mode=cv \
        --outdir=$RESULTS
