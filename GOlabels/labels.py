import hierarchyModule
import associationModule

hpath = "go-basic.obo.new"
apath = "dmelanogaster_systematic_associations.new.txt"
# apath = "dmelanogaster_systematic_associations.txt"

hm = hierarchyModule.hierarchyModule(hpath ,0)
am = associationModule.associationModule(apath)

def write_to(outpath, genes, namespace):
    print("Writing to namespace: {}".format(namespace))
    with open(outpath, 'w') as f:
        for g in genes:
            lbs = [hm.translate(x) for x in am.labels(g)]
            terms = [x for x in lbs if hm.inNamespace(x) == namespace]
            if terms == []:
                continue
            all_terms = set()
            for t in terms:
                all_terms = all_terms.union(hm.tricklesUp(t))
            all_terms = list(all_terms)
            all_terms.sort(key=lambda x: hm.levelOf(x))
            all_terms = [t + '@' + str(hm.levelOf(t)) for t in all_terms]
            f.write("{}\t{}\n".format(g, '\t'.join(all_terms)))


def main():
    print("Building modules...")

    genes = am.labeledGenes
    outprefix = './'
    nmspc = apath.split('/')[-1].split('.')[0]
    outpath_b = outprefix + nmspc + '.biological_process'
    outpath_f = outprefix + nmspc + '.molecular_function'
    outpath_c = outprefix + nmspc + '.cellular_component'

    write_to(outpath_b, genes, 'biological_process')
    write_to(outpath_f, genes, 'molecular_function')
    write_to(outpath_c, genes, 'cellular_component')    


if __name__ == "__main__":
    main()
