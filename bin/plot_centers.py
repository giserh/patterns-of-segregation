"""plot_centers.py

Plot the number of neighbourhoods as a function of city size
"""
from __future__ import division
import math
import csv
import numpy as np
from matplotlib import pylab as plt
import networkx as nx
from scipy.stats import linregress



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

## Number of neighbourhoods
number_neigh = {cl:{} for cl in classes}
with open('extr/neighbourhoods/numbers/numbers.csv', 'r') as source:
    reader =  csv.reader(source, delimiter='\t')
    cats = reader.next()[1:]
    for rows in reader:
        for i,clust in enumerate(rows[1:]):
            number_neigh[cats[i]][rows[0]] = float(clust)

## Number of households per MSA
households = {}
with open('data/population/msa/msa_households.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        households[rows[0]] = int(rows[1])



#
# Aggregate and fit
#
number = {cl:[number_neigh[cl][c] for c in households] for cl in classes}
population = [households[c] for c in households]

for cl in classes:
    print "Power-law fit for %s income class"%cl
    slope, intercept, r_value, p_value, std_err = linregress([math.log(p) for
        p in population],[math.log(d) for d in number[cl]])
    print "alpha = %s (R^2=%s)"%(slope, r_value)
#
# Plot the distribution
#
fig = plt.figure()
for i,cl in enumerate(classes):
    ax = fig.add_subplot(1, len(classes), i+1)
    ax.plot(population, number[cl], 'o', color=colours[cl], lw=2,
            mec=colours[cl],label=r"$%s$"%cl)
    ax.set_xlabel(r'$H$', fontsize=20)
    ax.set_ylabel(r'$N_{neighbourhoods}$', fontsize=20)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_position(('outward', 10))  # outward by 10 points
    ax.spines['bottom'].set_position(('outward', 10))  # outward by 10 points
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['bottom'].set_smart_bounds(True)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.legend(loc='upper left', numpoints=1, frameon=False)
plt.savefig('figures/paper/number.pdf', bbox_inches='tight')
plt.show()

