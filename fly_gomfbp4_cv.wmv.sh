# fly_gomfbp4_cv.wmv.sh

RESULTS=sep17_fly_results/

# MV CASCADE 

# gomfpb4 - 2fold - wmv all 
python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all \
        --rounds=12 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=$RESULTS

# gomfpb4 - 4fold - wmv all 
python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all \
        --rounds=12 \
        --cv_rounds=4 \
        --mode=cv \
        --outdir=$RESULTS

# gomfpb4 - 6fold - wmv all 
python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all \
        --rounds=12 \
        --cv_rounds=6 \
        --mode=cv \
        --outdir=$RESULTS

# gomfpb4 - 2fold - wmv known
python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=known \
        --rounds=12 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=$RESULTS

# gomfpb4 - 4fold - wmv known
python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=known \
        --rounds=12 \
        --cv_rounds=4 \
        --mode=cv \
        --outdir=$RESULTS

# gomfpb4 - 6fold - wmv known
python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=known \
        --rounds=12 \
        --cv_rounds=6 \
        --mode=cv \
        --outdir=$RESULTS

