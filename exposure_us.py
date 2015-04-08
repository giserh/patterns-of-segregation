"""exposure_us.py

Compute the exposure of the different classes for the whole US
"""
import csv
import marble as mb

#
# Import household income distribution
#
households = {}
with open('data/income/us/household_incomes.csv', 'r') as source:
    reader = csv.reader(source, delimiter=',')
    reader.next()
    for rows in reader:
        households[rows[1]] = {i:int(r) for i,r in enumerate(rows[7:])}



#
# Compute the exposure values and variance
#
exp = mb.exposure(households)



#
# Save the results
#

## Save the exposure values
with open('extr/exposure/categories/us/%s_values.csv'%city, 'w') as output:
    output.write("CATEGORIES\t" + "\t".join(map(str,range(num_cat))) + "\n")
    for c0 in sorted(exp.iterkeys()):
        output.write("%s\t"%c0)
        output.write("\t".join(map(str,[exp[c0][c1][0] for c1 in
                                sorted(exp[c0].iterkeys())])))
        output.write("\n")

## Save the exposure variance
with open('extr/exposure/categories/us/%s_variance.csv'%city, 'w') as output:
    output.write("CATEGORIES\t" + "\t".join(map(str,range(num_cat))) + "\n")
    for c0 in sorted(exp.iterkeys()):
        output.write("%s\t"%c0)
        output.write("\t".join(map(str,[exp[c0][c1][1] for c1 in
                                sorted(exp[c0].iterkeys())])))
        output.write("\n")

