# make pickles dir if necc.
mkdir -p pickles

# define yeast cDSD and mips labels filenames
FLY_DSD_FILE="cDSD/biogrid35170.dmelanogaster.cdsd"
GO_MFBP4="sampledata/fly_associations_bp.txt.pruned"

# make FLY-GOMFBPG4 pickle
echo "making fly GO-MFBP4 pickle..."
python3 run.py \
        --infile=$FLY_DSD_FILE \
        --type=DSD \
        --labelfile=$GO_MFBP4 \
        --labeltype=GO-MFBP4 \
        --name=fly.gomfpb4.dsd
