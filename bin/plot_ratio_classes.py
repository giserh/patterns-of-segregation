"""plot_ratio_classes.py

Plot the proportion of households that belong to a given class as a function of the
total number of households.
"""
from __future__ import division
import csv
from math import log10
import math
import numpy as np
from matplotlib import pylab as plt
from scipy.stats import linregress


colours = {'Lower':'#4F8F6B',
        'Higher':'#C1A62E',
        'Middle':'#4B453C'}

style = {'Lower':'s-',
        'Higher':'o-',
        'Middle':'#4B453C'}

# Puerto-rican cities are excluded from the analysis
PR_cities = ['7442','0060','6360','4840']


#
# Read data 
#

## List of MSA
msa = {}
with open('data/names/msa.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        if rows[0] not in PR_cities:
            msa[rows[0]] = rows[1]

## Classes
classes = {}
with open('extr/classes/msa_average/classes.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        classes[rows[0]] =[int(r) for r in rows[1:]]


## Number of households per class, and total
ratio_class = {cl:[] for cl in classes}
households = []
for i, city in enumerate(msa):
    print "Compute number of households for %s (%s/%s)"%(msa[city],
                                                        i+1,
                                                        len(msa))

    ## Import households data
    incomes = {}
    with open('data/income/msa/%s/income.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        reader.next()
        for rows in reader:
            num_cat = len(rows[1:])
            incomes[rows[0]] = {cl: sum([int(rows[1+c]) for c in classes[cl]])
                                        for cl in classes}
    incomes_cl = {cl: sum([incomes[au][cl] for au in incomes]) 
                                            for cl in classes}

    for cl in classes:
        ratio_class[cl].append( incomes_cl[cl]/sum(incomes_cl.values()) )
    households.append(sum(incomes_cl.values()))



#
# Plot
#
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
for i,cl in enumerate(classes):
    #
    # Bin data
    #
    ar_ratio = np.array(ratio_class[cl])
    ar_households = np.array(households)
    Nbins =20 
    bins = np.logspace(log10(min(households)), log10(max(households)), Nbins)
    digitized = np.digitize(households, bins)
    ratio_mean = [ar_ratio[digitized==i].mean() for i in range(1,len(bins)+1)]
    household_mean = [ar_households[digitized==i].mean() for i in
            range(1,len(bins)+1)]
    ratio_std = [ar_ratio[digitized==i].std()/len(ar_ratio[digitized==i]) for i in range(1,len(bins)+1)]
    
    #
    # Clean
    #
    # Clean the NaN values out
    household_clean, ratio_clean = zip(* filter( lambda x: not np.isnan(x[1]),
                                    zip(household_mean, ratio_mean) ))
    
    #
    # Plot
    #
    ax.plot(household_clean, ratio_clean, style[cl], color=colours[cl],
            mec=colours[cl], label=r'$%s$'%cl, lw=2.5)
    ax.fill_between(household_mean, 
                    [a-b for a,b in zip(ratio_mean,ratio_std)],
                    [a+b for a,b in zip(ratio_mean,ratio_std)],
                    color=colours[cl],
                    alpha=.5)



ax.set_xlabel(r'$H$', fontsize=20)
ax.set_ylabel(r'$\eta_i$', fontsize=20)
ax.set_xscale('log')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('outward', 10))  # outward by 10 points
ax.spines['bottom'].set_position(('outward', 10))  # outward by 10 points
ax.spines['left'].set_smart_bounds(True)
ax.spines['bottom'].set_smart_bounds(True)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.set_xlim([min(household_mean)/2, max(household_mean)*2])
ax.legend(loc='upper left', numpoints=1, frameon=False)
plt.savefig('figures/paper/si/ratio_classes.pdf', bbox_inches='tight')
plt.show()
