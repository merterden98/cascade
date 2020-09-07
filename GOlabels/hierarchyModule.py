import networkx as nx

biological_process = "GO:0008150"
molecular_function = "GO:0003674"
cellular_component = "GO:0005575"

class hierarchyModule:
    
    '''
      To initialize a hierarchyModule, specify:
         1. rawFilePath: absolute path to the .obo GO ontology file path
         2. pruneDepth: the number of levels from the root to discount
    '''
    def __init__(self, rawFilePath: str, pruneDepth: int):
        self.rawFilePath = rawFilePath
        self.pruneDepth = pruneDepth
        self.p = nx.DiGraph()
        self.f = nx.DiGraph()
        self.c = nx.DiGraph()
        self.altids = dict()
        self.info = dict()
        self.namespace = dict()
        self.obsoletes = set()
        self.__buildDag__()

    def __buildDag__(self):
        with open(self.rawFilePath, 'r') as f:
           terms = f.read().split("[Typedef]\n")[0].split("[Term]\n")[1:]
           for term in terms:
               data = term.strip().split('\n')
               goID = data[0].strip()[4:]
               self.info[goID] = data
               if "is_obsolete: true" in data:
                   self.obsoletes.add(goID)
               alts = [x for x in data if "alt_id: " in x]
               for alt in alts:
                   x = alt.split(': ')[1]
                   self.altids[x] = goID
               namespace = data[2].strip().split(': ')[1]
               self.namespace[goID] = namespace
               parents = [x.split(" ! ")[0].split(": ")[1] for x in data if "is_a: " in x]

               if namespace == "biological_process":
                   self.__addEdges__(self.p, goID, parents)
               elif namespace == "molecular_function":
                   self.__addEdges__(self.f, goID, parents)
               elif namespace == "cellular_component":
                   self.__addEdges__(self.c, goID, parents)
               else:
                   print("Cannot determine namespace for " + goID)
        if self.pruneDepth == 0:
            self.excluded = []
            return
        else:
            self.pruneDepth = self.pruneDepth - 1 # because we are using SSSP to determine depth        

        self.excluded = list(nx.single_source_shortest_path(self.p, biological_process, self.pruneDepth))
        self.excluded.extend(list(nx.single_source_shortest_path(self.f, molecular_function, self.pruneDepth)))
        self.excluded.extend(list(nx.single_source_shortest_path(self.c, cellular_component, self.pruneDepth)))

    def __addEdges__(self, graph, child, parents):
        for parent in parents:
            graph.add_edge(parent, child)

    '''
      Given a node, decides whether it is discounted based on 
      the predetermined pruneDepth
    '''
    def isExcluded(self, node):
        return node in self.excluded

    '''
      Given a node, returns the information associated with it
      in the original .obo file
    '''
    def getInfo(self, node):
        return self.info[node]

    '''
      Given a node, returns its level in the ontology, which is
      defined as the length of the single source shortest path from
      its root node
    '''
    def levelOf(self, node):
        if self.namespace[node] == "biological_process":
            root_node = biological_process
            tree = self.p
        elif self.namespace[node] == "molecular_function":
            root_node = molecular_function
            tree = self.f
        elif self.namespace[node] == "cellular_component":
            root_node = cellular_component
            tree = self.c
        else:
            print("invalid GO term")
        
        return nx.shortest_path_length(tree, root_node, node)

    '''
      Given a node, returns the namespace it is in
    '''       
    def inNamespace(self, node):
        return self.namespace[node]

    '''
      Given an id, returns the main id
    '''    
    def translate(self, node):
        if node in self.altids:
            return self.altids[node]
        else:
            return node    

    '''
      Given a node, return it along with all of its ancestors 
      that are not excluded, discounting obsolete GO terms
    '''
    def tricklesUp(self, node):
        if node in self.obsoletes:
            return set()
        if node in self.altids:
            return self.tricklesUp(self.altids[node])

        if self.namespace[node] == "biological_process":
            tree = self.p
        elif self.namespace[node] == "molecular_function":
            tree = self.f
        elif self.namespace[node] == "cellular_component":
            tree = self.c
        else:
            print("invalid GO term")
        
        ancestors_list = set([x for x in nx.ancestors(tree, node) if x not in self.excluded])

        return ancestors_list.union(set([node]))
