"""neighbourhoods_numbers.py

Compute the number of neighbourhoods and concerned areal units for all 2000
MSA.
"""
from __future__ import division
import csv
import networkx as nx



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
neigh_num = {}
for i, city in enumerate(msa):
    print "Compute the number of neighbourhoods for %s (%s/%s)"%(msa[city],
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
    neigh_num[city] = {cl: len(list(neighbourhoods[cl])) for cl in classes}



#
# Save the data
#
with open('extr/neighbourhoods/numbers/numbers.csv', 'w') as output:
    output.write('MSA FIP')
    for cl in sorted(classes):
        output.write('\tNeighbourhoods %s'%cl)
    output.write('\n')
    for city in neigh_num:
        output.write(str(city))
        for cl in sorted(classes):
            output.write('\t%s'%neigh_num[city][cl])
        output.write('\n')
