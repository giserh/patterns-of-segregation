"""plot_inter-urban.py

Plot the representation of the different classes as a function of the size of
the city.
"""
from __future__ import division
import csv
import math
import marble as mb
from matplotlib import pylab as plt


#
# Parameters
#
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



## Number of people per income class per MSA
distribution = {}
households = {}
for city in msa:

    # Import category composition
    income = {}
    with open('data/income/msa/%s/income.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        reader.next()
        for rows in reader:
            categories = range(len(rows[1:]))
            income[rows[0]] = {c:int(h) for c,h in enumerate(rows[1:])}
    
    # Aggregate all
    distribution[city] = {c:sum([income[bg][c] for bg in income]) for c in categories}
    households[city] = sum(distribution[city].values())




#
# Get the over and under representation figures 
#

## Country-wide representation
representation = mb.representation(distribution, classes)

## Representation in order of population
over = {cl:[] for cl in classes}
under = {cl:[] for cl in classes}
normal = {cl:[] for cl in classes}
for city in sorted(msa, key=lambda x: households[x]):
    for cl in classes:
        delta = representation[city][cl][0] - 1
        sigma = math.sqrt(representation[city][cl][1]) 
        if abs(delta) <= 2.57*sigma:
            over[cl].append(0)
            under[cl].append(0)
            normal[cl].append(1)
        else:
            if delta < 0:
                over[cl].append(0)
                under[cl].append(1)
                normal[cl].append(0)
            else:
                over[cl].append(1)
                under[cl].append(0)
                normal[cl].append(0)

## Population (in terms of households)
pop = sorted(households.values())

## Cumulative
over_sup = {cl:[sum(over[cl][i:])/len(pop[i:]) for i in range(len(pop))] 
                for cl in classes}
under_sup = {cl:[sum(under[cl][i:])/len(pop[i:]) for i in range(len(pop))]
                for cl in classes}
ok_sup = {cl: [sum(normal[cl][i:])/len(pop[i:]) for i in range(len(pop))]
                for cl in classes}



#
# Plot
#
fig = plt.figure()
ax = fig.add_subplot(111)
for i,cl in enumerate(classes):
    ax.plot(pop,over_sup[cl],"-", lw=2, color=colours[cl], mec=None,
                label=r"$%s$"%cl)
ax.set_xlim([5300, 7711000])
ax.set_ylim([-0.01, 1.01])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('outward', 10))  # outward by 10 points
ax.spines['bottom'].set_position(('outward', 10))  # outward by 10 points
ax.spines['left'].set_smart_bounds(True)
ax.spines['bottom'].set_smart_bounds(True)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.set_ylabel(r"$\frac{N_{\alpha}^{>}(H)}{N^{>}(H)}$",fontsize=25)
ax.set_xlabel(r"$H$",fontsize=25)
ax.set_xscale('log')
ax.legend(loc='best', numpoints=1,bbox_to_anchor=(1.0, 1.0), frameon=False)
plt.axhline(y=0.5, linestyle='--', color='black')
plt.savefig('figures/paper/inter-urban_representation.pdf', bbox_inches='tight')
plt.show()
