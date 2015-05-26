"""plot_scaling_income.py

Plot the scaling of the total income versus the total number of households.
"""
import csv
import math
from matplotlib import pylab as plt
from scipy.stats import linregress



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


## total number of households and income per msa 
households = []
income = []
income_d = {}
households_d = {}
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
            incomes[rows[0]] = {c: int(num) for c,num in enumerate(rows[1:])}


    ## aggregate
    income.append(sum([sum([incomes[au][cl]*income_bins[cl] for cl in incomes[au]])
                                                        for au in incomes]))
    income_d[city] = sum([sum([incomes[au][cl]*income_bins[cl] for cl in incomes[au]])
                                                        for au in incomes])

    households.append(sum([sum([incomes[au][cl] for cl in incomes[au]])
                                      for au in incomes]))
    households_d[city] = sum([sum([incomes[au][cl] for cl in incomes[au]])
                                      for au in incomes])


#
# Fit
#
print "Power-law fit"
slope, intercept, r_value, p_value, std_err = linregress([math.log(p) for
    p in households],[math.log(d) for d in income])
print "alpha=%s, R^2=%s"%(slope, r_value)

## Who are the worst outliers?
delta = {c:(income_d[c]) / \
            math.exp(intercept)*households_d[c]**slope for c in households_d}

print [msa[c] for c in households_d if households_d[c]==35612]

#
# Plot
#
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
ax.plot(households, income, 'o', color='black',
        mec='black')
ax.plot(sorted(households), 
        [math.exp(intercept)*h**slope for h in sorted(households)],
        label=r'$I \sim H^{\,%.2f}$'%(slope),
        linestyle='--',
        color='black')
ax.set_xlabel(r'$H$', fontsize=20)
ax.set_ylabel(r'$I$', fontsize=20)
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
plt.savefig('figures/paper/si/scaling_income.pdf', bbox_inches='tight')
plt.show()
