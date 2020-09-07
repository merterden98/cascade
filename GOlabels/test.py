with open("/r/bcb/GOlabels/data/associations/bioprocess.txt", 'r') as f:
    for line in f:
        goid, des, genes = line.split('\t')
        print(len(genes.split()))
