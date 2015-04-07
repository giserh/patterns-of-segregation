"""adjacency_blockgroups.py

Script to compute the adjacency list for the blockgroups in all MSA
"""
import csv
import sys
import itertools
import fiona
from shapely.geometry import shape


csv.field_size_limit(sys.maxsize)


#
# Import list of cities 
#
msa = {}
with open('data/names/msa.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        msa[rows[0]] = rows[1]



#
# Compute the adjacency list
#
for i,city in enumerate(msa):
    print "Adjacency %s (%s/%s)"%(msa[city], i+1, len(msa))

    ## Import blockgroups
    blocks = {}
    with fiona.open('data/shp/msa/%s/blockgroups.shp'%city, 'r', 'ESRI Shapefile') as source:
        for f in source:
            blocks[f['properties']['BKGPIDFP00']] = shape(f['geometry'])


    ## Compute adjacency list
    adjacency = {b:[] for b in blocks}
    for b0,b1 in itertools.permutations(blocks, 2):
        if blocks[b1].touches(blocks[b0]):
            adjacency[b0].append(b1)

    ## Save data
    with open('extr/adjacency_bg/msa/%s.csv'%city, 'w') as output:
       output.write("BLOCKGROUP FIP\tNEIGHBOURS FIP (list)\n")
       for b0 in adjacency:
           output.write("%s"%b0)
           for b1 in adjacency[b0]:
               output.write("\t%s"%b1)
           output.write("\n")
