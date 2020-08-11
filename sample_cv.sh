# sample_run.sh
# script for running CV on yeast graphs


# mips3;
python3 -i run.py --infile=pickles/yeast.pickle \
        --type=PICKLE \
        --vtype=MV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all \
        --rounds=12 \
        --cv_rounds=2 \
        --mode=predict \
        --outdir=raw_result/
#
## mips3 hierarchical
#python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
#        --type=PICKLE \
#        --vtype=MVH \
#        --conftype=ENT \
#        --threshold=0.35 \
#        --ntype=all_h \
#        --rounds=12 \
#        --cv_rounds=2 \
#        --mode=cv \
#        --outdir=raw_result/
#
#python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
#        --type=PICKLE \
#        --vtype=MV \
#        --conftype=ENT \
#        --threshold=0.35 \
#        --ntype=all \
#        --rounds=12 \
#        --cv_rounds=4 \
#        --mode=cv \
#        --outdir=raw_result/
#
## mips3 hierarchical
#python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
#        --type=PICKLE \
#        --vtype=MVH \
#        --conftype=ENT \
#        --threshold=0.35 \
#        --ntype=all_h \
#        --rounds=12 \
#        --cv_rounds=4 \
#        --mode=cv \
#        --outdir=raw_result/
#
## --------
#
## OLD:
## mips2;
## python3 run.py --infile=pickles/yeast.mips2.dsd.pickle \
##         --type=PICKLE \
##         --vtype=MV \
##         --conftype=ENT \
##         --threshold=0.3 \
##         --ntype=all \
##         --round=10 \
##         --cv_rounds=2 \
##         --mode=cv \
##         --outdir=raw_result/
#
## # mips3;
## python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
##         --type=PICKLE \
##         --vtype=MV \
##         --conftype=ENT \
##         --threshold=0.3 \
##         --ntype=all \
##         --round=10 \
##         --cv_rounds=2 \
##         --mode=cv \
##         --outdir=raw_result/
#
#
        
