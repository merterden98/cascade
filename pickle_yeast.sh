# make pickles dir if necc.
mkdir -p pickles

# define yeast cDSD and mips labels filenames
YEAST_DSD_FILE="sampledata/yeast.cdsd"
MIPS1="sampledata/MIPSFirstLevel.list"
MIPS2="sampledata/MIPSSecondLevel.list"
MIPS3="sampledata/MIPSThirdLevel.list"

# make mips1 pickle
# echo "making yeast mips1 pickle..."
# python3 run.py --infile=$YEAST_DSD_FILE \
#         --type=DSD --labelfile=$MIPS1 --labeltype=mips1 \
#         --hfiles $MIPS1 \
#         --name=yeast.mips1.dsd 

# make mips2 pickle
echo "making yeast mips2 pickle..."
python3 run.py --infile=$YEAST_DSD_FILE \
        --type=DSD --labelfile=$MIPS2 --labeltype=mips2 --hfiles $MIPS1 \
        --name=yeast.mips2.dsd 

# make mips3 pickle
echo "making yeast mips3 pickle..."
python3 run.py --infile=$YEAST_DSD_FILE \
        --type=DSD --labelfile=$MIPS3 --labeltype=mips3 --hfiles $MIPS2 $MIPS1 \
        --name=yeast.mips3.dsd



