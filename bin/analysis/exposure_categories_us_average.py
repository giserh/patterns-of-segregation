"""exposure_us_average.py

Script to compute the average exposure matrix for all cities in the US.
"""
from __future__ import division
import csv
import math


#
# Import a list of MSA
#
msa = {}
with open('data/names/msa.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        msa[rows[0]] = rows[1]



#
# Import the exposure for all cbsas in the dataset
# (As if all cities were put together in one large city)
#
exposure_values_all = {}
exposure_variance_all = {}
households_all = {}
N_all = {} 
for i, city in enumerate(msa):
    print "Import the exposure for %s|%s (%s/%s)"%(city,msa[city], i+1, len(msa))

    ## Import exposure values
    exposure_val = {}
    with open('extr/exposure/categories/msa/%s_values.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        categories = reader.next()[1:]
        for rows in reader:
            exposure_val[int(rows[0])] = {int(cat): float(val) for cat, val 
                                              in zip(categories, rows[1:])}
    ## Import exposure variance
    exposure_var = {}
    with open('extr/exposure/categories/msa/%s_variance.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        categories = reader.next()[1:]
        for rows in reader:
            exposure_var[int(rows[0])] = {int(cat): float(var) for cat, var 
                                              in zip(categories, rows[1:])}

    ## Import household income distribution
    households = {}
    with open('data/income/msa/%s/income.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        reader.next()
        for rows in reader:
            num_cat = len(rows[1:])
            households[rows[0]] = {c:int(h) for c,h in enumerate(rows[1:])}
            households_all[rows[0]] = {c:int(h) for c,h in enumerate(rows[1:])}
 
    N_MSA = sum([households[au][cl] for au in households for cl in households[au]])

    ## Compute total matrix
    categories = [c for c in range(num_cat)]
    for c0 in categories:
        if c0 not in N_all:
            N_all[c0] = {}
        for c1 in categories:
            if c1 not in N_all[c0]:
                N_all[c0][c1] = 0
            
            if c0 not in exposure_values_all:
                exposure_values_all[c0] = {c1:[] for c1 in categories}
            if not math.isnan(exposure_val[c0][c1]):
                exposure_values_all[c0][c1].append(N_MSA*exposure_val[c0][c1]) 
                N_all[c0][c1] += N_MSA

            if c0 not in exposure_variance_all:
                exposure_variance_all[c0] = {c1:[] for c1 in categories}
            if not math.isnan(exposure_var[c0][c1]):
                exposure_variance_all[c0][c1].append((N_MSA**2*(exposure_var[c0][c1])) 


#
# Compute the average matrix
#
exposure_average_value = {c0: {c1:sum(exposure_values_all[c0][c1])/N_all[c0][c1]
                                for c1 in categories}
                         for c0 in categories}

exposure_average_variance = {c0 : {c1: math.sqrt(sum(exposure_variance_all[c0][c1])
                                                 / N_all[c0][c1]**2)
                                  for c1 in categories}
                            for c0 in categories}


## Concatenate values
exp = {c0: {c1: (exposure_average_value[c0][c1],
                 exposure_average_variance[c0][c1])
            for c1 in categories}
       for c0 in categories}




#
# Save the average exposure
#

## Save the exposure values
with open('extr/exposure/categories/us/msa_average/values.csv', 'w') as output:
    output.write("CATEGORIES\t" + "\t".join(map(str,range(num_cat))) + "\n")
    for c0 in sorted(exp.iterkeys()):
        output.write("%s\t"%c0)
        output.write("\t".join(map(str,[exp[c0][c1][0] for c1 in
                                sorted(exp[c0].iterkeys())])))
        output.write("\n")

## Save the exposure variance
with open('extr/exposure/categories/us/msa_average/variance.csv', 'w') as output:
    output.write("CATEGORIES\t" + "\t".join(map(str,range(num_cat))) + "\n")
    for c0 in sorted(exp.iterkeys()):
        output.write("%s\t"%c0)
        output.write("\t".join(map(str,[exp[c0][c1][1] for c1 in
                                sorted(exp[c0].iterkeys())])))
        output.write("\n")
