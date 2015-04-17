"""clustering.py

Compute the normalised clustering coefficient for all 2000
MSA.
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
clusterings = {}
for i, city in enumerate(msa):
    print "Compute clustering for %s (%s/%s)"%(msa[city],
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


    ## Extract neighbourhoods (the connected components of the subgraph
    ## constituted of the areal units where the class is overrepresented)
    neighbourhoods = {cl: nx.connected_component_subgraphs(G.subgraph(over_bg[cl]))
                        for cl in classes}
    num_neighbourhoods = {cl: len(list(neighbourhoods[cl])) for cl in classes}

    ## Compute clustering
    clustering = {}
    for cl in classes:
        if len(over_bg[cl]) == 0:
            clustering[cl] = float('nan')
        elif len(over_bg[cl]) == 1:
            clustering[cl] = 1
        else:
            clust = num_neighbourhoods[cl] / len(over_bg[cl])
            clustering[cl] = 1 - ((clust-(1/len(over_bg[cl]))) / 
                                    (1-(1/len(over_bg[cl]))))

    clusterings[city] = clustering




#
# Save the data
#
with open('extr/clustering/classes/clustering.csv', 'w') as output:
    output.write('MSA FIP')
    for cl in sorted(classes):
        output.write('\t%s'%cl)
    output.write('\n')
    for city in clusterings:
        output.write(str(city))
        for cl in sorted(classes):
            output.write('\t%s'%clusterings[city][cl])
        output.write('\n')
