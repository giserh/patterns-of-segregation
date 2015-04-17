"""neighbourhoods_content.py

Compute the neighbourhoods relative content in terms of population for all
class, for all cities.
"""
from __future__ import division
import csv


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
ratios = {}
for i, city in enumerate(msa):
    print "Compute neighbourhoods content for %s (%s/%s)"%(msa[city],
                                                        i+1,
                                                        len(msa))

    ## Import the distribution of households in the various blockgroups
    households = {}
    with open('data/income/msa/%s/income.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        reader.next()
        for rows in reader:
            households[rows[0]] = {c:int(h) for c,h in enumerate(rows[1:])}

    income = {bg:{cl:sum([households[bg][c] for c in classes[cl]]) for cl in classes}
            for bg in households} 
    H_class = {cl: sum([income[bg][cl] for bg in income]) for cl in classes}


    ## Import list of bg where each class is overrepresented
    over_bg = {cl:[] for cl in classes}
    with open('extr/neighbourhoods/classes/msa/%s.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        for rows in reader:
            over_bg[rows[0]].append(rows[1])

    ## Compute the ratios
    ratios[city] = {cl:sum([income[bg][cl] for bg in over_bg[cl]]) / H_class[cl]
            for cl in classes}



#
# Save the data
#
with open('extr/neighbourhoods/content/content.csv', 'w') as output:
    output.write('MSA FIP')
    for cl in sorted(classes):
        output.write('\t%s'%cl)
    output.write('\n')
    for city in ratios:
        output.write(str(city))
        for cl in sorted(classes):
            output.write('\t%s'%ratios[city][cl])
        output.write('\n')
