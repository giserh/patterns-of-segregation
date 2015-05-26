"""plot_income_scaling.py

Plot the number of households from a given class as a function of the total
number of households per city
"""
import csv
import math
from matplotlib import pylab as plt
from scipy.stats import linregress


colours = {'Lower':'#4F8F6B',
        'Higher':'#C1A62E',
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
households_class = {cl:[] for cl in classes}
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
        households_class[cl].append(incomes_cl[cl])
    households.append(sum(incomes_cl.values()))


#
# Fit
#
slopes = {}
r_values = {}
intercepts = {}
for cl in classes:
    print "Power-law fit for %s income class"%cl
    slope, intercept, r_value, p_value, std_err = linregress([math.log(p) for
        p in households],[math.log(d) for d in households_class[cl]])
    slopes[cl] = slope
    r_values[cl] = r_value
    intercepts[cl] = intercept
    print "alpha = %s (R^2=%s)"%(slope, r_value)

#
# Plot
#
fig = plt.figure(figsize=(24,8))
for i,cl in enumerate(classes):
    ax = fig.add_subplot(1, len(classes), i+1)
    ax.plot(households, households_class[cl], 'o', color=colours[cl],
            mec=colours[cl], label=r'$%s$'%cl)
    ax.plot(sorted(households), 
            [math.exp(intercepts[cl])*h**slopes[cl] for h in sorted(households)],
            label=r'$H_{%s} \sim H^{\,%.2f}$'%(cl, slopes[cl]),
            linestyle='--',
            color='black')
    ax.set_xlabel(r'$H$', fontsize=20)
    ax.set_ylabel(r'$H_{%s}$'%cl, fontsize=20)
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
plt.savefig('figures/paper/si/scaling_class.pdf', bbox_inches='tight')
plt.show()
