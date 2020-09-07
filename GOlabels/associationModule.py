class associationModule:
    
    '''
      To initialize an associationModule, specify:
        1. rawFilePath: absolute path to the GO association files path
    '''
    def __init__(self, rawFilePath: str):
        self._labels = dict()
        self._descriptions = dict()
        self._labeledGenes = set()
        self._unlabeledGenes = set()
        self.labeledGenes = list()    # a list of labeled genes
        self.__read__(rawFilePath)       


    def __read__(self, path):
        with open(path, 'r') as f:
            for line in f:
                if line[0] != '#' and line[0] == 'G':
                    goID, description, genes = line.strip().split('\t')
                    self._descriptions[goID] = description
                    genes = genes.split()
                    for g in genes:
                        self._labeledGenes.add(g)
                        if g in self._labels:
                            self._labels[g].add(goID)
                        else:
                            self._labels[g] = set([goID])
                elif line[0] != '#':
                    self._unlabeledGenes = set(line.strip().split())
        self.labeledGenes = list(self._labeledGenes)

    '''
      elaborate(term) returns the English description for a given 
      valid GO term
    '''
    def elaborate(self, term):
        if term in self._descriptions:
            return self._descriptions[term]
        else:
           print("{} is not a valid GO term.".format(term))
    
    '''
      is_labeled(g) returns whether the given gene is labeled with
      at least one GO term
    '''
    def isLabeled(self, g):
        return g in self._labeledGenes

    '''
      is_in_genespace(g) returns whether the given gene is contained
      in the GO association file, labeled or unlabeled
    '''
    def isInGenespace(self, g):
        return self.isLabeled(g) or g in self._unlabeledGenes
       
    '''
      labels(g) returns all GO terms associated with the gene
    '''
    def labels(self, g):
        if self.isLabeled(g):
            return self._labels[g]
        elif self.isOnGenespace(g):
            return set()
        else:
            print("Gene not in genespace")


