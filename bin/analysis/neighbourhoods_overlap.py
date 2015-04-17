"""neighbourhoods_overlap.py

Compute the overlap between the different neighbourhoods.
"""
from __future__ import division
import csv
import networkx as nx
from matplotlib import pylab as plt



#
# Preparation
#

## List of MSA
msa = {}
with open('data/names/msa.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        msa[rows[0]] = rows[1]

## Classes
classes = {}
with open('extr/classes/msa_average/classes.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        classes[rows[0]] =[int(r) for r in rows[1:]]



#
# Compute the clustering value
#
overlaps = {}
for i, city in enumerate(msa):
    print "Compute overlaps for %s (%s/%s)"%(msa[city],
                                                i+1,
                                                len(msa))

    ## Import adjacency matrix
    adjacency = {}
    with open('extr/adjacency_bg/msa/%s.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        reader.next()
        for rows in reader:
            adjacency[rows[0]] = rows[1:]


    ## Transform into graph
    G = nx.from_dict_of_lists(adjacency)


    ## Import list of bg where each class is overrepresented
    over_bg = {cl:[] for cl in classes}
    with open('extr/neighbourhoods/classes/msa/%s.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        for rows in reader:
            over_bg[rows[0]].append(rows[1])


    overlaps[city] = {cl0: {cl1: len(set(over_bg[cl0]).intersection(set(over_bg[cl1]))) /
                                 min([len(over_bg[cl0]), len(over_bg[cl1])])
                            for cl1 in classes if cl1!=cl0} 
                    for cl0 in classes}



#
# Save the data
#
with open('extr/neighbourhoods/overlap/overlap.csv', 'w') as output:
    output.write('MSA FIP')
    for i,cl0 in enumerate(classes.keys()):
        for cl1 in classes.keys()[i+1:]:
            output.write('\t%s-%s'%(cl0, cl1))
    output.write('\n')
    for city in overlaps:
        output.write(str(city))
        for i,cl0 in enumerate(classes.keys()):
            for cl1 in classes.keys()[i+1:]:
                output.write('\t%s'%(overlaps[city][cl0][cl1]))
        output.write('\n')
