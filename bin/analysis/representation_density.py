"""representation_density_percolation.py

Compute the representation of the different classes inside/outside percolation
clusters as the density threshold is increased.
"""
from __future__ import division
import csv
import marble as mb


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
# Compute the high/low density percolation
#
for i,city in enumerate(msa):
    print "Compute representations and density for %s (%s/%s)"%(msa[city],
                                                                i+1,
                                                                len(msa))
    
    ## Import blockgroup area
    area = {}
    with open('data/surface_area/blockgroups/%s_blockgroup_area.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        reader.next()
        for rows in reader:
            area[rows[0]] = float(rows[1]) / 1000000 #in km^2


    ## Import blockgroup income distribution
    households = {}
    with open('data/income/msa/%s/income.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        reader.next()
        for rows in reader:
            categories = range(len(rows[1:]))
            households[rows[0]] = {c:int(h) for c,h in enumerate(rows[1:])}

    H_block = {bg:sum(households[bg].values()) for bg in households}


    ## Compute population density
    density = {bg:H_block[bg] / area[bg] for bg in H_block}

    ## Compute representation
    representation = mb.representation(households, classes)


    #
    # Save the data
    #
    with open('extr/representation/classes/density/%s_density.csv'%city,
            'w') as output:
        output.write('Blockgroup FIP\tDensity (/km^2)')
        for cl in sorted(classes):
            output.write('\tRepresentation %s\tVariance %s'%(cl,cl))

        output.write('\n')
        for bg in sorted(density, key=lambda x:density[x], reverse=1):
            rho = density[bg]
            output.write(str(bg)+'\t'+str(rho))
            for cl in sorted(classes):
                output.write('\t%s\t%s'%(representation[bg][cl][0],
                                         representation[bg][cl][1]))
            output.write('\n')
