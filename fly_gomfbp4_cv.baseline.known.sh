# fly_gomfbp4_cv.sh

RESULTS=sep_results/


# MV  NO CASCADE BASELINES 

# gomfpb4 - 2fold - mv known 
python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
        --type=PICKLE \
        --vtype=MV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=known \
        --rounds=1 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=$RESULTS

# gomfpb4 - 4fold - mv known 
python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
        --type=PICKLE \
        --vtype=MV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=known \
        --rounds=1 \
        --cv_rounds=4 \
        --mode=cv \
        --outdir=$RESULTS

# gomfpb4 - 6fold - mv known 
python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
        --type=PICKLE \
        --vtype=MV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=known \
        --rounds=1 \
        --cv_rounds=6 \
        --mode=cv \
        --outdir=$RESULTS


# WMV Baselines

# gomfpb4 - 2fold - mv known 
python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=known \
        --rounds=1 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=$RESULTS

# gomfpb4 - 4fold - mv known 
python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=known \
        --rounds=1 \
        --cv_rounds=4 \
        --mode=cv \
        --outdir=$RESULTS

# gomfpb4 - 6fold - mv known 
python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
        --type=PICKLE \
        --vtype=WMV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=known\
        --rounds=1 \
        --cv_rounds=6 \
        --mode=cv \
        --outdir=$RESULTS
