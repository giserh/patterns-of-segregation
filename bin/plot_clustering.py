"""plot_clustering.py

Plot the distribution of the renormalised clustering coefficient for all 2000
MSA.
"""
from __future__ import division
import csv
import numpy as np
from matplotlib import pylab as plt
import networkx as nx



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

## Clustering values
clustering = {cl:[] for cl in classes}
with open('extr/clustering/classes/clustering.csv', 'r') as source:
    reader =  csv.reader(source, delimiter='\t')
    cats = reader.next()[1:]
    for rows in reader:
        for i,clust in enumerate(rows[1:]):
            clustering[cats[i]].append(float(clust))


#
# Plot the distribution
#
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
for cl in classes:
    print "Clustering for %s"%cl
    print np.mean(clustering[cl])
    
    ## Bin the data
    cs = np.array(clustering[cl])
    N_bins = 20
    bins = np.linspace(min(cs), max(cs), N_bins)
    l_bin = (max(cs)-min(cs)) / N_bins
    m = np.mean(cs)
    s = np.std(cs)
    digitized = np.digitize(cs, bins)
    cs_mean = [cs[digitized == i].mean() for i in range(1, len(bins))]
    cs_counts = [0 for i in range(len(bins))]
    for d in digitized:
        cs_counts[d-1] += 1/(len(cs)*l_bin)

    # Clean the NaN values out
    cs_clean, counts_clean = zip(* filter( lambda x: not np.isnan(x[0]),
                                    zip(cs_mean,cs_counts[1:]) ))
    ax.plot(cs_clean, counts_clean, 'k-', color=colours[cl], lw=3,
            label=r"$%s$"%cl)
    ax.set_xlabel(r'$C$', fontsize=30)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_position(('outward', 10))  # outward by 10 points
    ax.spines['bottom'].set_position(('outward', 10))  # outward by 10 points
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['bottom'].set_smart_bounds(True)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.legend(loc='upper left', numpoints=1, frameon=False, fontsize=15)
plt.savefig('figures/paper/clustering.pdf', bbox_inches='tight')
plt.show()

