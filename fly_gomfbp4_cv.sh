# fly_gomfbp4_cv.sh

RESULTS=sep7_fly_results/

# MV CASCADE 

# gomfpb4 - 2fold - mv all 
python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
        --type=PICKLE \
        --vtype=MV \
        --conftype=CT \
        --threshold=0.35 \
        --ntype=all \
        --rounds=12 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=$RESULTS

# # gomfpb4 - 4fold - mv all 
# python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
#         --type=PICKLE \
#         --vtype=MV \
#         --conftype=CT \
#         --threshold=0.35 \
#         --ntype=all \
#         --rounds=12 \
#         --cv_rounds=4 \
#         --mode=cv \
#         --outdir=$RESULTS

# # gomfpb4 - 6fold - mv all 
# python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
#         --type=PICKLE \
#         --vtype=MV \
#         --conftype=CT \
#         --threshold=0.35 \
#         --ntype=all \
#         --rounds=12 \
#         --cv_rounds=6 \
#         --mode=cv \
#         --outdir=$RESULTS

# # gomfpb4 - 2fold - mv known
# python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
#         --type=PICKLE \
#         --vtype=MV \
#         --conftype=CT \
#         --threshold=0.35 \
#         --ntype=known \
#         --rounds=12 \
#         --cv_rounds=2 \
#         --mode=cv \
#         --outdir=$RESULTS

# # gomfpb4 - 4fold - mv known
# python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
#         --type=PICKLE \
#         --vtype=MV \
#         --conftype=CT \
#         --threshold=0.35 \
#         --ntype=known \
#         --rounds=12 \
#         --cv_rounds=4 \
#         --mode=cv \
#         --outdir=$RESULTS

# # gomfpb4 - 6fold - mv known
# python3 run.py --infile=pickles/fly.gomfbp4.dsd.pickle \
#         --type=PICKLE \
#         --vtype=MV \
#         --conftype=CT \
#         --threshold=0.35 \
#         --ntype=known \
#         --rounds=12 \
#         --cv_rounds=6 \
#         --mode=cv \
#         --outdir=$RESULTS

