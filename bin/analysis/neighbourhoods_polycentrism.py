"""neighbourhoods_polycentrism

Compute the ratio of the size of the two largest neighbourhoods for all 2000
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
ratio_size = {}
for i, city in enumerate(msa):
    print "Compute clustering for %s (%s/%s)"%(msa[city],
                                                i+1,
                                                len(msa))

    ## Import distribution 
    households = {}
    with open('data/income/msa/%s/income.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        reader.next()
        for rows in reader:
            households[rows[0]] = {c:int(h) for c,h in enumerate(rows[1:])}

    income = {bg:{cl:sum([households[bg][c] for c in classes[cl]]) for cl in classes}
            for bg in households} 


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
    neighbourhoods = {cl: [[n for n in subgraph] 
                        for subgraph in nx.connected_component_subgraphs(G.subgraph(over_bg[cl]))]
                        for cl in classes}

    neigh_pops = {cl: [sum([income[bg][cl] for bg in neigh]) for neigh in neighbourhoods[cl]]
                    for cl in classes}

    ratio_size[city] = {cl: (sorted(neigh_pops[cl], reverse=1)[1] / 
                            max(neigh_pops[cl])) 
                            if len(neigh_pops[cl]) > 1 else 0
                        for cl in classes}
#
# Save the data
#
with open('extr/neighbourhoods/polycentrism/polycentrism.csv', 'w') as output:
    output.write('MSA FIP')
    for cl in sorted(classes):
        output.write('\t%s'%cl)
    output.write('\n')
    for city in ratio_size:
        output.write(str(city))
        for cl in sorted(classes):
            output.write('\t%s'%ratio_size[city][cl])
        output.write('\n')
