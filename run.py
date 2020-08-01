import argparse
import pickle
from os import path, mkdir
from src import makegraph
from src import crossvalidate

parser = argparse.ArgumentParser(description='Run Majority Vote Cascading'
                                 ' on a network with labels')
parser.add_argument('--infile', help='Network Embedding File', required=True)
parser.add_argument('--type',
                    choices=['DSD', 'PPI', 'PICKLE'],
                    help='Network Embedding Type',
                    required=True)
parser.add_argument('--labelfile',
                    help='Protein Label file if not in PICKLE mode')
parser.add_argument('--labeltype',
                    help='Label type (i.e. mips1, mips2, etc.)', default="MIPS")

parser.add_argument('--name',
                    help='object name for pickling')

parser.add_argument(
    '--vtype', choices=['MV', 'WMV', 'MVH', 'WMVH'], default='WMV')
parser.add_argument('--conftype', choices=['ENT', 'CT', 'WCT'], default='ENT')
parser.add_argument('--threshold',
                    type=float,
                    default=0.30,
                    help='confidence threshold value')
parser.add_argument('--K',
                    type=int,
                    default=10,
                    help='number of neighbors for kNN')
parser.add_argument('--ntype',
                    choices=['all', 'known', 'all_h'],
                    default='known')
parser.add_argument('--rounds', type=int, default=10)
parser.add_argument('--cv_rounds', type=int, default=2)
parser.add_argument('--hfiles',
                    nargs='+',
                    help='Files containing extra MIPS label information')
parser.add_argument('--mode', choices=['cv', 'predict'], default='predict')
parser.add_argument('--outdir', default='./')


def main():
    args = parser.parse_args()

    # GRAPH GENERATION LOGIC
    ppi_graph = None

    if args.type == 'PICKLE':
        ppi_graph = pickle.load(open(args.infile, 'rb'))

    if args.type != 'PICKLE':
        if not args.labelfile:
            raise Exception('Need label file for non Pickle graphs')
        else:
            if args.type == 'DSD':
                # Refactor for GO
                ppi_graph = makegraph.getPPIGraph(args.infile, args.labelfile,
                                                  args.labeltype, args.type,
                                                  args.hfiles)
                if not path.isdir('./pickles'):
                    mkdir('./pickles')

                pickle.dump(ppi_graph, open(
                    "pickles/{}.pickle".format(args.name), 'wb'))

            if args.type == 'PPI':
                raise Exception('Needs Implementation')

    if ppi_graph:
        if args.mode == 'predict':
            crossvalidate.predict(ppigraph=ppi_graph,
                                  voting_type=args.vtype,
                                  conf_type=args.conftype,
                                  K=args.K,
                                  nb_type=args.ntype,
                                  cascade_rounds=args.rounds)
        if args.mode == 'cv':
            print("Running CV")
            print(args.infile)
            crossvalidate.run_cv_tests(ppigraph=ppi_graph,
                                       voting_type=args.vtype,
                                       conf_type=args.conftype,
                                       K=args.K,
                                       nb_type=args.ntype,
                                       cascade_rounds=args.rounds,
                                       conf_threshold=args.threshold,
                                       cv_splits=args.cv_rounds,
                                       outfile=args.outdir,
                                       labels=ppi_graph.label_type)


if __name__ == '__main__':
    main()
