"""
pickle_graphs.py

A script for pickling PPIGraph objects based on label and metric type
"""
import pickle
from src import makegraph

# -----------------------------------------------------------------------------
#                            DATA PATHS
#

# cDSD Matrices
yeast_cdsd_fname = "data/biogrid35170.scerevisiae.cdsd"
fly_cdsd_fname = "data/biogrid35170.dmelanogaster.cdsd"

string_cdsd_fname = "string/string_4932.dsd"

# GO labels
gobp3_inf_fname = "data/scerevisiae_GO_inf.bp3"
yeast_mfbp3_inf_fname = "data/scerevisiae_GO_inf.mfbp3"
fly_mfbp3_inf_fname = "data/dmelanogaster_GO_inf.mfbp3"
yeast_mfbp3_inf4_fname = "data/scerevisiae_GO_inf_level4.mfbp3"
fly_mfbp3_inf4_fname = "data/dmelanogaster_GO_inf_level4.mfbp3"

# NEW gomfbp names
yeast_mfbp3_inf5_fname = "data/scerevisiae_GO_inf_level5.mfbp3"
yeast_mfbp3_inf6_fname = "data/scerevisiae_GO_inf_level6.mfbp3"

fly_mfbp3_inf5_fname = "data/dmelanogaster_GO_inf_level5.mfbp3"
fly_mfbp3_inf6_fname = "data/dmelanogaster_GO_inf_level6.mfbp3"


# MIPS labels
mips1_fname = "data/MIPSFirstLevel.list"
mips2_fname = "data/MIPSSecondLevel.list"
mips3_fname = "data/MIPSThirdLevel.list"

# YEAST - MF and BP union
'''
yeast_cdsd_gomfbp3_l5_inf = makegraph.generate_graph_DSD(dsd_filename=yeast_cdsd_fname,
                                                      labels_filename=yeast_mfbp3_inf5_fname,
                                                      label_type="GO-mfbp-inf-L5-35170",
                                                      metric_type="CDSD")

pickle.dump(yeast_cdsd_gomfbp3_l5_inf, open("pickles/cdsd_gomfbp3_infL5_35170.pkl", 'wb'))

yeast_cdsd_gomfbp3_l6_inf = makegraph.generate_graph_DSD(dsd_filename=yeast_cdsd_fname,
                                                      labels_filename=yeast_mfbp3_inf6_fname,
                                                      label_type="GO-mfbp-inf-L6-35170",
                                                      metric_type="CDSD")

pickle.dump(yeast_cdsd_gomfbp3_l6_inf, open("pickles/cdsd_gomfbp3_infL6_35170.pkl", 'wb'))

yeast_cdsd_gomfbp3_l4_inf_str = makegraph.generate_graph_DSD(dsd_filename=string_cdsd_fname,
                                                             labels_filename=yeast_mfbp3_inf4_fname,
                                                             label_type="GO-mfbp-inf-L4-4932",
                                                             metric_type="CDSD")

pickle.dump(yeast_cdsd_gomfbp3_l4_inf_str, open("cdsd_gomfbp3_infL4_4932.pkl", 'wb'))
'''
# FLY - MF and BP union
'''
fly_cdsd_gomfbp3_l5_inf = makegraph.generate_graph_DSD(dsd_filename=fly_cdsd_fname,
                                                       labels_filename=fly_mfbp3_inf5_fname,
                                                       label_type="GO-FLY-mfbp3-inf-L5-35170",
                                                       metric_type="CDSD")

pickle.dump(fly_cdsd_gomfbp3_l5_inf, open("pickles/cdsd_FLY_gomfbp3_infL5_35170.pkl", 'wb'))

fly_cdsd_gomfbp3_l6_inf = makegraph.generate_graph_DSD(dsd_filename=fly_cdsd_fname,
                                                       labels_filename=fly_mfbp3_inf6_fname,
                                                       label_type="GO-FLY-mfbp3-inf-L6-35170",
                                                       metric_type="CDSD")

pickle.dump(fly_cdsd_gomfbp3_l6_inf, open("pickles/cdsd_FLY_gomfbp3_infL6_35170.pkl", 'wb'))
'''

# -----------------------------------------------------------------------------
#                      GENERATE GRAPHS + PICKLE - YEAST
#
"""
#CDSD with GO labels

cdsd_gobp3_inf = makegraph.generate_graph_DSD(dsd_filename=cdsd_fname,
                                              labels_filename=gobp3_inf_fname,
                                              label_type="GO-bp3-inf-35170",
                                              metric_type="CDSD")

pickle.dump(cdsd_gobp3_inf, open("pickles/cdsd_gobp3_inf_35170.pkl", 'wb'))

# CDSD with MIPS1 labels

cdsd_mips1 = makegraph.generate_graph_DSD(dsd_filename=cdsd_fname,
                                               labels_filename=mips1_fname,
                                               label_type="mips1-35170",
                                               metric_type="CDSD")

pickle.dump(cdsd_mips1, open("pickles/cdsd_mips1_35170.pkl", 'wb'))

cdsd_mips2 = makegraph.generate_graph_DSD(dsd_filename=cdsd_fname,
                                               labels_filename=mips2_fname,
                                               label_type="mips2-35170",
                                               metric_type="CDSD")

pickle.dump(cdsd_mips2, open("pickles/cdsd_mips2_35170.pkl", 'wb'))
"""
cdsd_mips3 = makegraph.generate_graph_DSD(dsd_filename=yeast_cdsd_fname,
                                          labels_filename=mips3_fname,
                                          label_type="mips3-35170",
                                          hierarchy_labels=[mips3_fname, mips2_fname, mips1_fname],
                                          metric_type="CDSD")

pickle.dump(cdsd_mips3, open("pickles/cdsd_mips3_35170.pkl", 'wb'))


# FLY ----------------------------------------------------

# cDSD Matrices
# cdsd_fname = "data/biogrid35170.dmelanogaster.cdsd"

# # GO labels
# gobp3_inf_fname = "data/dmelanogaster_GO_inf.bp3"

# """CDSD with GO labels"""

# cdsd_gobp3_inf = makegraph.generate_graph_DSD(dsd_filename=cdsd_fname,
#                                               labels_filename=gobp3_inf_fname,
#                                               label_type="fly-GO-bp3-inf-35170",
#                                               metric_type="CDSD")

# pickle.dump(cdsd_gobp3_inf, open("pickles/cdsd_FLY_gobp3_inf_35170.pkl", 'wb'))
