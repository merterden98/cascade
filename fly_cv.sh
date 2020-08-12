RESULTS=aug03_results_fly/

# -------------------------------------------------------
#                  Updated GO Fly Exp                    #
mkdir $RESULTS
python3 run.py --infile=pickles/new_fly.pickle \
        --type=PICKLE \
        --vtype=MV \
        --conftype=ENT \
        --threshold=0.35 \
        --ntype=all \
        --rounds=12 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=$RESULTS \
        --name=new_fly

#python3 run.py --infile=pickles/fly_associations_bpmf.pickle \
#        --type=PICKLE \
#        --vtype=MV \
#        --conftype=ENT \
#        --threshold=0.35 \
#        --ntype=known \
#        --rounds=12 \
#        --cv_rounds=4 \
#        --mode=cv \
#        --outdir=$RESULTS \
#        --name=tmp
#
#python3 run.py --infile=pickles/fly_associations_bpmf.pickle \
#        --type=PICKLE \
#        --vtype=MV \
#        --conftype=ENT \
#        --threshold=0.35 \
#        --ntype=known \
#        --rounds=12 \
#        --cv_rounds=6 \
#        --mode=cv \
#        --outdir=$RESULTS \
#        --name=tmp
#        
#python3 run.py --infile=pickles/fly_associations_bpmf.pickle \
#        --type=PICKLE \
#        --vtype=WMV \
#        --conftype=ENT \
#        --threshold=0.35 \
#        --ntype=known \
#        --rounds=12 \
#        --cv_rounds=2 \
#        --mode=cv \
#        --outdir=$RESULTS \
#        --name=tmp
#
#python3 run.py --infile=pickles/fly_associations_bpmf.pickle \
#        --type=PICKLE \
#        --vtype=WMV \
#        --conftype=ENT \
#        --threshold=0.35 \
#        --ntype=known \
#        --rounds=12 \
#        --cv_rounds=4 \
#        --mode=cv \
#        --outdir=$RESULTS \
#        --name=tmp
#
#python3 run.py --infile=pickles/fly_associations_bpmf.pickle \
#        --type=PICKLE \
#        --vtype=WMV \
#        --conftype=ENT \
#        --threshold=0.35 \
#        --ntype=known \
#        --rounds=12 \
#        --cv_rounds=6 \
#        --mode=cv \
#        --outdir=$RESULTS \
#        --name=tmp
#
#python3 run.py --infile=pickles/fly_associations_bpmf.pickle \
#        --type=PICKLE \
#        --vtype=MV \
#        --conftype=ENT \
#        --threshold=0.35 \
#        --ntype=all \
#        --rounds=12 \
#        --cv_rounds=2 \
#        --mode=cv \
#        --outdir=$RESULTS \
#        --name=tmp
#
#python3 run.py --infile=pickles/fly_associations_bpmf.pickle \
#        --type=PICKLE \
#        --vtype=MV \
#        --conftype=ENT \
#        --threshold=0.35 \
#        --ntype=all \
#        --rounds=12 \
#        --cv_rounds=4 \
#        --mode=cv \
#        --outdir=$RESULTS \
#        --name=tmp
#
#python3 run.py --infile=pickles/fly_associations_bpmf.pickle \
#        --type=PICKLE \
#        --vtype=MV \
#        --conftype=ENT \
#        --threshold=0.35 \
#        --ntype=all \
#        --rounds=12 \
#        --cv_rounds=6 \
#        --mode=cv \
#        --outdir=$RESULTS \
#        --name=tmp
#
#
#
#python3 run.py --infile=pickles/fly_associations_bpmf.pickle \
#        --type=PICKLE \
#        --vtype=WMV \
#        --conftype=ENT \
#        --threshold=0.35 \
#        --ntype=all \
#        --rounds=12 \
#        --cv_rounds=2 \
#        --mode=cv \
#        --outdir=$RESULTS \
#        --name=tmp
#
#python3 run.py --infile=pickles/fly_associations_bpmf.pickle \
#        --type=PICKLE \
#        --vtype=WMV \
#        --conftype=ENT \
#        --threshold=0.35 \
#        --ntype=all \
#        --rounds=12 \
#        --cv_rounds=4 \
#        --mode=cv \
#        --outdir=$RESULTS \
#        --name=tmp
#
#python3 run.py --infile=pickles/fly_associations_bpmf.pickle \
#        --type=PICKLE \
#        --vtype=WMV \
#        --conftype=ENT \
#        --threshold=0.35 \
#        --ntype=all \
#        --rounds=12 \
#        --cv_rounds=6 \
#        --mode=cv \
#        --outdir=$RESULTS \
#        --name=tmp