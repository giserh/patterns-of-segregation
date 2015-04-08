"""exposure_categories.py

Compute the exposure between the different categories for each MSA.
The isolation is given by the diagonal terms of the matrix.
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
            num_cat = len(rows[1:])
            households[rows[0]] = {c:int(h) for c,h in enumerate(rows[1:])}
    
    ## Compute the exposure (and isolation)
    exp = mb.exposure(households)

    ## Save the exposure values
    with open('extr/exposure/categories/msa/%s_values.csv'%city, 'w') as output:
        output.write("CATEGORIES\t" + "\t".join(map(str,range(num_cat))) + "\n")
        for c0 in sorted(exp.iterkeys()):
            output.write("%s\t"%c0)
            output.write("\t".join(map(str,[exp[c0][c1][0] for c1 in
                                    sorted(exp[c0].iterkeys())])))
            output.write("\n")

    ## Save the exposure variance
    with open('extr/exposure/categories/msa/%s_variance.csv'%city, 'w') as output:
        output.write("CATEGORIES\t" + "\t".join(map(str,range(num_cat))) + "\n")
        for c0 in sorted(exp.iterkeys()):
            output.write("%s\t"%c0)
            output.write("\t".join(map(str,[exp[c0][c1][1] for c1 in
                                    sorted(exp[c0].iterkeys())])))
            output.write("\n")
