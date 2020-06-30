# make pickles dir if necc.
mkdir -p pickles

# define yeast cDSD and mips labels filenames
YEAST_DSD_FILE="cDSD/biogrid35170.scerevisiae.cdsd"
MIPS1="sampledata/MIPSFirstLevel.list"
MIPS2="sampledata/MIPSSecondLevel.list"
MIPS3="sampledata/MIPSThirdLevel.list"
HDATA=sampledata/*.list

# make mips1 pickle
echo "making yeast mips1 pickle..."
python3 run.py --infile=$YEAST_DSD_FILE --type=DSD --labelfile=$MIPS1 --name=yeast.mips1.dsd --hfiles $HDATA

# make mips2 pickle
echo "making yeast mips2 pickle..."
python3 run.py --infile=$YEAST_DSD_FILE --type=DSD --labelfile=$MIPS2 --name=yeast.mips1.dsd --hfiles $HDATA

# make mips3 pickle
echo "making yeast mips3 pickle..."
python3 run.py --infile=$YEAST_DSD_FILE --type=DSD --labelfile=$MIPS1 --name=yeast.mips1.dsd --hfiles $HDATA



