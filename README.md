# Majority Vote Cascading

This repository provides the reference implementation of Majority Vote Cascading as described in the paper:

> Majority Vote Cascading: A Semi-Supervised Framework for Improving Protein Function Prediction.<br>
> Lazarsfeld et al.

### Usage

TODO: Need to allow users to pass in graph from a file and return labelled nodes in text file.

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
└── test_acc.py
```
