RESULTS=aug03_results/go/

# -------------------------------------------------------
#                  MIPS 2 - 2fold cv                    #

# mips2 - 2fold - mv all ;
python3 run.py --infile=pickles/flybp.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all \
        --rounds=12 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=$RESULTS \
        --name=tmp