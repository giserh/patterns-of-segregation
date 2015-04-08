"""neighbourhoods_categories.py

Find the tracts where each category is over-represented or all cities in the
dataset.
"""
import csv
import marble as mb


#
# Import a list of MSA
#
msa = {}
with open('data/names/msa.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        msa[rows[0]] = rows[1]


#
# Extract neighbourhoods and save
#
for i, city in enumerate(msa):
    print "Extract neighbourhoods for %s (%s/%s)"%(msa[city],
                                                i+1,
                                                len(msa))

    ## Import households data
    households = {}
    with open('data/income/msa/%s/income.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        reader.next()
        for rows in reader:
            households[rows[0]] = {c:int(h) for c,h in enumerate(rows[1:])}


    ## Extract neighbourhoods
    neigh = mb.overrepresented_units(households)

    ## Save the list of areal units per class
    with open('extr/neighbourhoods/categories/msa/%s.csv'%city, 'w') as output:
        for cat in sorted(neigh.iterkeys()):
            for bkgp in neigh[cat]:
                output.write("%s\t%s\n"%(cat, bkgp))
