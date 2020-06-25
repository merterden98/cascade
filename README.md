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
├── __init__.py
├── fly_annotate.py
├── informative_go.py
├── pickle_graphs.py
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
