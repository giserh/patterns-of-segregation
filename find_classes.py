"""find_classes.py

Script to find the emergent classes from the values of the exposure previously
measured
"""
from __future__ import division
import csv
import math
import marble as mb


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
N_all = 0
for i, city in enumerate(msa):
    print "Import the exposure for %s|%s (%s/%s)"%(city,msa[city], i+1, len(msa))

    ## Import exposure values
    exposure_val = {}
    with open('extr/exposure/categories/msa/%s_values.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        categories = reader.next()[1:]
        for rows in reader:
            exposure_val[rows[0]] = {cat: float(val) for cat, val 
                                              in zip(categories, rows[1:])}
    ## Import exposure variance
    exposure_var = {}
    with open('extr/exposure/categories/msa/%s_variance.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        for rows in reader:
            exposure_var[rows[0]] = {cat: float(var) for cat, var 
                                              in zip(categories, rows[1:])}

    ## Import household income distribution
    households = {}
    with open('data/income/msa/%s/income.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        reader.next()
        for rows in reader:
            num_cat = len(rows[1:])
            households[rows[0]] = {c:int(h) for c,h in enumerate(rows[1:])}
            households_all[rows[0]] = households[rows[0]]

    N_MSA = sum([households[au][cl] for au in households for cl in households[au]])
    N_all += N_MSA

    ## Compute total matrix
    categories = [str(c) for c in range(num_cat)]
    for c0 in categories:
        for c1 in categories:

            if c0 not in exposure_values_all:
                exposure_values_all[c0] = {c1:[] for c1 in categories}
            exposure_values_all[c0][c1].append(N_MSA*exposure_val[c0][c1]) 

            if c0 not in exposure_variance_all:
                exposure_variance_all[c0] = {c1:[] for c1 in categories}
            exposure_variance_all[c0][c1].append((N_MSA*exposure_var[c0][c1])**2) 


#
# Compute the average matrix
#
exposure_average_value = {c0: {c1: sum(exposure_values_all[c0][c1])/N_all
                                for c1 in categories}
                         for c0 in categories}
exposure_average_variance = {c0 : {c1: math.sqrt(sum(exposure_variance_all[c0][c1])
                                                 / N_all**2)
                                  for c1 in categories}
                            for c0 in categories}

exposure_average = {c0: {c1: (exposure_average_value, exposure_average_variance)
                        for c1 in categories}
                    for c0 in categories}


#
# Get the linkage matrix
#
link = mb.cluster_categories(households, exposure_average)
