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

## High densities
density_high = []
representation_high = {cl:[] for cl in classes}
for city in msa:
    data_path = 'extr/representation/classes/density_percolation/%s_high-density.csv'%city
    with open(data_path, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        reader.next()
        for rows in reader:
            density_high.append(float(rows[0]))
            for j,cl in enumerate(sorted(classes)):
                representation_high[cl].append(float(rows[j*2+1]))


## Low densities
density_low = []
representation_low = {cl:[] for cl in classes}
for city in msa:
    data_path = 'extr/representation/classes/density_percolation/%s_low-density.csv'%city
    with open(data_path, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        reader.next()
        for rows in reader:
            density_low.append(float(rows[0]))
            for j,cl in enumerate(sorted(classes)):
                representation_low[cl].append(float(rows[j*2+1]))


#
# Bin the data according to density
#

## High densities 
cs = np.array(density_high)
N_bins = 60 
#bins = np.linspace(min(cs), max(cs), N_bins)
bins = np.logspace(1, log(max(cs)), N_bins)
l_bin = (max(cs)-min(cs)) / N_bins
m = np.mean(cs)
s = np.std(cs)
digitized = np.digitize(cs, bins)
density_high_mean = [cs[digitized == i].mean() for i in range(1, len(bins))]
mean_rep_high = {}
for cl in classes:
    mean_rep_high[cl] = [np.array(representation_high[cl])[digitized==i].mean() 
                            for i in range(1,len(bins))]

## Low densities 
cs = np.array(density_low)
N_bins = 60 
#bins = np.linspace(min(cs), max(cs), N_bins)
bins = np.logspace(1, log(max(cs)), N_bins)
l_bin = (max(cs)-min(cs)) / N_bins
m = np.mean(cs)
s = np.std(cs)
digitized = np.digitize(cs, bins)
density_low_mean = [cs[digitized == i].mean() for i in range(1, len(bins))]
mean_rep_low = {}
for cl in classes:
    mean_rep_low[cl] = [np.array(representation_low[cl])[digitized==i].mean() 
                            for i in range(1,len(bins))]



#
# Plot
#
fig = plt.figure()

## High densities zones
ax = fig.add_subplot(121)
for cl in classes:
    ax.plot(density_high_mean, mean_rep_high[cl], '-', 
            color=colours[cl],
            lw=2)
ax.axhline(y=1, linestyle='--', color='black')
ax.set_xlabel(r'$\rho_T\,(km^{-2})$', fontsize=20)
ax.set_ylabel(r'$r_\alpha$', fontsize=20)
ax.set_title(r'$High\,densities$', fontsize=20)
ax.set_xscale('log')
ax.set_ylim([0.6, 1.5])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('outward', 10))  # outward by 10 points
ax.spines['bottom'].set_position(('outward', 10))  # outward by 10 points
ax.spines['left'].set_smart_bounds(True)
ax.spines['bottom'].set_smart_bounds(True)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')


## Low density zones

# Plot
ax = fig.add_subplot(122)
for cl in classes:
    # Clean the NaN values out
    density_clean,mean_rep_clean = zip(* filter( lambda x: not np.isnan(x[1]),
                                        zip(density_low_mean,mean_rep_low[cl]) ))
    ax.plot(density_clean, mean_rep_clean, '-', 
            color=colours[cl],
            label=r'$%s$'%cl,
            lw=2)
ax.axhline(y=1, linestyle='--', color='black')
ax.set_xlabel(r'$\rho_T\,(km^{-2})$', fontsize=20)
ax.set_ylabel(r'$r_\alpha$', fontsize=20)
ax.set_title(r'$Low\,densities$', fontsize=20)
ax.set_xscale('log')
ax.set_ylim([0.6, 1.5])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('outward', 10))  # outward by 10 points
ax.spines['bottom'].set_position(('outward', 10))  # outward by 10 points
ax.spines['left'].set_smart_bounds(True)
ax.spines['bottom'].set_smart_bounds(True)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.legend(loc='upper right', numpoints=1, frameon=False)
plt.savefig('figures/paper/percolation.pdf', bbox_inches='tight')
plt.show()
