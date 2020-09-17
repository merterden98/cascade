# Majority Vote Cascading

This repository provides the reference implementation of Majority Vote Cascading as described in the paper:

> Majority Vote Cascading: A Semi-Supervised Framework for Improving Protein Function Prediction.<br>
> Lazarsfeld et al.

### Usage

Note MVC currently works with only DSD file formats.

All functionality can be accessed via `run.py` and requires
user to specify either a predict mode or a cross validation
mode.

Below is the bare minimum if one desires to predict a collection
of functional labels.

```shell
>>> python3 run.py --mode predict --infile [MATRIX FILE] --labelfile [PROTEIN LABEL FILE] --type [TYPE_OF_EMBEDDING]
```

See `python3 run.py -h` for extra optional arguments such as selection of confidence functions and voting functions.

In cross validation mode, N-Fold cross validation is run on provided graph and statistics are reported to user specified location. It is defaulted to current file location.

Below is a more complicated example.
It will run MVC in cross validation mode on yeast data. Hierarchy mips files are also provided for hierarchical voting. **`--ntype` must be set to `all_h` for hierarchical voting to take place.**

```shell
>>> python3 ./run.py --mode cv --infile=/data/yeast.cdsd --type=DSD --labelfile=/data/MIPSThirdLevel.list --hfiles /data/MIPSSecondLevel.list /data/MIPSFirstLevel.list --vtype=MVH --ntype=all_h
```

### File Structure

```shell
├── README.md
├── data
├── src
│   ├── __init__.py
│   ├── cascade.py -- Functions for manipulating pseudolabels
│   ├── confidence.py -- Contains confidence functions
│   ├── crossvalidate.py -- Testing Suite
│   ├── graph.py -- PPIGraph class for usage in makegraph.py
│   ├── makegraph.py -- Functions for creating PPIGraph
│   └── vote.py -- Contains polymorphic vote functions
└── run.py
```

### Data files

The `data` sub-directory contains the following raw data files used during CV experiments:
* `biogrid35170.scerevisiae.PPI`: *S. cerevisiae* PPIs from BioGRID with confidence values
* `biogrid35170.dmelanogaster.PPI`: *D. melanogaster* PPIs from BioGRID with confidence values
* `MIPSFirstLevel.list, MIPSSecondLevel.list, MIPSThirdLevel.list`: MIPS annotations for *S. cerevisiae* 
* `scerevisiae_GO_inf.mfbp4, dmelanogaster_GO_inf.new.mfbp4`: informative GO annotations (see paper methodology for details) for *S. cerevisiae* and *D. melanogaster*, respectively. 

Code used to generate cDSD matrices can be found on the [cDSD website](http://dsd.cs.tufts.edu/capdsd/)

