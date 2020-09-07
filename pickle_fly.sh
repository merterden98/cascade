# make pickles dir if necc.
mkdir -p pickles

# define yeast cDSD and mips labels filenames
# FLY_DSD_FILE="cDSD/biogrid35170.dmelanogaster.cdsd"
# GO_MFBP4="flydata/dmelanogaster_GO_inf.mfbp4"

# # make FLY-GOMFBPG4 pickle
# echo "making fly GO-MFBP4 pickle..."
# python3 run.py \
#         --infile=$FLY_DSD_FILE \
#         --type=DSD \
#         --labelfile=$GO_MFBP4 \
#         --labeltype=GO-MFBP4 \
#         --name=fly.gomfbp4.dsd

FLY_DSD_FILE="cDSD/biogrid35170.dmelanogaster.cdsd"
GO_MFBP4="flydata/dmelanogaster_GO_inf_level4.OLD.mfbp3"

# make FLY-GOMFBPG4 pickle
echo "making fly GO-MFBP4 pickle..."
python3 run.py \
        --infile=$FLY_DSD_FILE \
        --type=DSD \
        --labelfile=$GO_MFBP4 \
        --labeltype=GO-MFBP4 \
        --name=fly.gomfbp4.OLD.dsd
