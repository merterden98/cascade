# sample_run.sh
# script for running CV on yeast graphs

# mips1;
python3 run.py --infile=pickles/yeast.mips1.dsd.pickle \
        --type=PICKLE \
        --vtype=MV \
        --conftype=ENT \
        --threshold=0.3 \
        --ntype=all \
        --round=10 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=raw_result/


# mips2;
python3 run.py --infile=pickles/yeast.mips2.dsd.pickle \
        --type=PICKLE \
        --vtype=MV \
        --conftype=ENT \
        --threshold=0.3 \
        --ntype=all \
        --round=10 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=raw_result/

# mips3;
python3 run.py --infile=pickles/yeast.mips3.dsd.pickle \
        --type=PICKLE \
        --vtype=MV \
        --conftype=ENT \
        --threshold=0.3 \
        --ntype=all \
        --round=10 \
        --cv_rounds=2 \
        --mode=cv \
        --outdir=raw_result/


        
