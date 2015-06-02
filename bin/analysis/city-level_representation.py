"""city-level_representation.py

Compute the representation of the different classes in the city as a whole,
compared to the US.
"""
from __future__ import division
import csv
import math
import marble as mb
from matplotlib import pylab as plt


#
# Parameters
#
colours = {'Lower':'#4F8F6B',
        'Higher':'#C1A62E',
        'Middle':'#4B453C'}




#
# Import data
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



## Number of people per income class per MSA
distribution = {}
households = {}
for city in msa:

    # Import category composition
    income = {}
    with open('data/income/msa/%s/income.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        reader.next()
        for rows in reader:
            categories = range(len(rows[1:]))
            income[rows[0]] = {c:int(h) for c,h in enumerate(rows[1:])}
    
    # Aggregate all
    distribution[city] = {c:sum([income[bg][c] for bg in income]) for c in categories}
    households[city] = sum(distribution[city].values())




#
# Get the over and under representation figures 
#

## Country-wide representation
representation = mb.representation(distribution, classes)

## Representation in order of population
# 1 if overrepresented, 0 if normal, -1 if underrepresented
rep = {city: {} for city in msa}
for city in sorted(msa, key=lambda x: households[x]):
    for cl in classes:
        delta = representation[city][cl][0] - 1
        sigma = math.sqrt(representation[city][cl][1]) 
        if abs(delta) <= 2.57*sigma:
            rep[city][cl] = 0
        else:
            if delta < 0:
                rep[city][cl] = -1
            else:
                rep[city][cl] = 1

#
# Write the data
#
with open('extr/representation/us/city-level_representation.py', 'w') as output:
    output.write('MSA FIP\tMSA Name')
    for cl in classes:
        output.write('\t%s'%cl)
    output.write('\n')
    for city in rep:
        output.write('%s\t%s'%(city, msa[city]))
        for cl in classes:
            output.write('\t%s'%rep[city][cl])
        output.write('\n')
