RESULTS=aug_results/

# -------------------------------------------------------
#                  Updated GO Fly Exp                    #
mkdir $RESULTS
python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
        --type=PICKLE \
        --vtype=MV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all \
        --rounds=12 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=$RESULTS \

