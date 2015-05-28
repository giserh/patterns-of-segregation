"""households_per_class.py

Count the number of households per class across the US
"""
from __future__ import division
import csv



#
# Read the data
#

## Classes
classes = {}
with open('extr/classes/msa_average/classes.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        classes[rows[0]] =[int(r) for r in rows[1:]]

## Income data at block-group level
incomes = {}
with open('data/income/us/household_incomes.csv', 'r') as source:
    reader = csv.reader(source, delimiter=',')
    reader.next()
    for rows in reader:
        incomes[rows[1]] = {cl:sum([int(rows[7+i]) for i in classes[cl]])
                                                    for cl in classes}


#
# Compute the number of households per class
#
N_class = {cl: sum([incomes[au][cl] for au in incomes]) for cl in classes}
N_tot = sum(N_class.values())

for cl in classes:
    print "%s: "%cl, N_class[cl]/N_tot
