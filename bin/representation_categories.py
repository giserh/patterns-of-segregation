"""category_representation.py

Compute the representation of the original categories in the dataset and the
variance obtained for the null model.
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
# Extract and save the data
#
for j, city in enumerate(msa):
    print "Extract the representation of categories for %s (%s/%s)"%(city,
                                                                    j+1,
                                                                    len(msa))


    ## Import category composition
    households = {}
    with open('data/income/msa/%s/income.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        reader.next()
        for rows in reader:
            households[rows[0]] = {c:int(h) for c,h in enumerate(rows[1:])}

    ## Compute representation and variance
    rep = mb.representation(households) 

    ## Save the values
    with open('extr/representation/categories/msa/%s_values.csv'%city, 'w') as output:
        output.write('BLOCKGROUP FIP\n')
        for bg in rep:
            output.write(str(bg))
            for cat in sorted(rep[bg].iterkeys()):
                val, var = rep[bg][cat]
                output.write('\t%s'%val)
            output.write('\n')

    ## Save the variance
    with open('extr/representation/categories/msa/%s_variance.csv'%city, 'w') as output:
        output.write('BLOCKGROUP FIP\n')
        for bg in rep:
            output.write(str(bg))
            for cat in sorted(rep[bg].iterkeys()):
                val, var = rep[bg][cat]
                output.write('\t%s'%var)
            output.write('\n')

