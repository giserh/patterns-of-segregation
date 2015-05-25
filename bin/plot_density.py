"""plot_percolation.py

Plot the average representation of the different classes as a function of
density for all MSA
"""
import csv
from math import log
import numpy as np
from matplotlib import pylab as plt



colours = {'Lower':'#4F8F6B',
        'Higher':'#C1A62E',
        'Middle':'#4B453C'}



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
# Import data
#

density = []
representation = {cl:[] for cl in classes}
for city in msa:
    data_path = 'extr/representation/classes/density/%s_density.csv'%city
    with open(data_path, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        reader.next()
        for rows in reader:
            density.append(float(rows[1]))
            for j,cl in enumerate(sorted(classes)):
                representation[cl].append(float(rows[j*2+2]))



#
# Bin the data according to density
#

## High densities 
cs = np.array(density)
N_bins = 60 
#bins = np.linspace(min(cs), max(cs), N_bins)
bins = np.logspace(1, log(max(cs)), N_bins)
l_bin = (max(cs)-min(cs)) / N_bins
m = np.mean(cs)
s = np.std(cs)
digitized = np.digitize(cs, bins)
density_mean = [cs[digitized == i].mean() for i in range(1, len(bins))]
mean_rep = {}
for cl in classes:
    mean_rep[cl] = [np.array(representation[cl])[digitized==i].mean() 
                            for i in range(1,len(bins))]

#
# Plot
#
fig = plt.figure(figsize=(12,8))

## High densities zones
ax = fig.add_subplot(111)
for cl in classes:
    ax.plot(density_mean, mean_rep[cl], '-', 
            label=r'$%s$'%cl,
            color=colours[cl],
            lw=3)
ax.axhline(y=1, linestyle='--', color='black')
ax.set_xlabel(r'$\rho\,(km^{-2})$', fontsize=30)
ax.set_ylabel(r'$\overline{r}\left(\rho\right)$', fontsize=30)
ax.set_xscale('log')
#ax.set_ylim([0.6, 1.5])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('outward', 10))  # outward by 10 points
ax.spines['bottom'].set_position(('outward', 10))  # outward by 10 points
#ax.spines['left'].set_smart_bounds(True)
ax.spines['bottom'].set_smart_bounds(True)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.legend(loc='upper left', numpoints=1, frameon=False, fontsize=15)
plt.savefig('figures/paper/density.pdf', bbox_inches='tight')
plt.show()
