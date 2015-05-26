"""plot_gini.py

Plot the Gini of the income distribution as a function of the number of
households in cities.
"""
from __future__ import division
import csv
import numpy as np
import itertools
from matplotlib import pylab as plt

#
# Parameters and functions
#
income_bins = [1000,12500,17500,22500,27500,32500,37500,42500,47500,55000,70000,90000,115000,135000,175000,300000]

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


#
# Compute gini for all msa
#
gini = []
households = []
for n, city in enumerate(msa):
    print "Compute Gini index for %s (%s/%s)"%(msa[city], n+1, len(msa))

    ## Import households income
    data = {}
    with open('data/income/msa/%s/income.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        reader.next()
        for rows in reader:
            num_cat = len(rows[1:])
            data[rows[0]] = {c:int(h) for c,h in enumerate(rows[1:])}

    # Sum over all areal units
    incomes = {cat:sum([data[au][cat] for au in data]) for cat in range(num_cat)}


    ## Compute the Gini index
    # See Dixon, P. M.; Weiner, J.; Mitchell-Olds, T.; and Woodley, R. 
    # "Bootstrapping the Gini Coefficient of Inequality." Ecology 68, 1548-1551, 1987.
    g = 0
    pop = 0
    for a,b in itertools.permutations(incomes, 2):
        g += incomes[a]*incomes[b]*abs(income_bins[a]-income_bins[b])
    pop = sum([incomes[a] for a in incomes])
    average = sum([incomes[a]*income_bins[a] for a in incomes])/pop
    gini.append((1/(2*pop**2*average))*g)
    households.append(pop)



#
# Plot
#

fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
ax.plot(households, gini, 'o', color='black', mec='black')
ax.set_xlabel(r'$H$', fontsize=30)
ax.set_ylabel(r'$Gini$', fontsize=30)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('outward', 10))  # outward by 10 points
ax.spines['bottom'].set_position(('outward', 10))  # outward by 10 points
ax.spines['left'].set_smart_bounds(True)
ax.spines['bottom'].set_smart_bounds(True)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.set_xscale('log')
plt.savefig('figures/paper/si/gini_income.pdf', bbox_inches='tight')
plt.show()
