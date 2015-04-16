"""representation_classes.py

Compute the representation of the emergent classes in the dataset and the
variance obtained for the null model.
"""
import csv
import marble as mb


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



#
# Extract and save the data
#
for j, city in enumerate(msa):
    print "Extract the representation of classes for %s (%s/%s)"%(city,
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
    rep = mb.representation(households, classes) 

    ## Save the values
    with open('extr/representation/classes/msa/%s_values.csv'%city, 'w') as output:
        output.write('BLOCKGROUP FIP')
        for cl in sorted(classes.iterkeys()):
            output.write('\t%s'%cl)
        output.write('\n')
        for bg in rep:
            output.write(str(bg))
            for cat in sorted(rep[bg].iterkeys()):
                val, var = rep[bg][cat]
                output.write('\t%s'%val)
            output.write('\n')

    ## Save the variance
    with open('extr/representation/classes/msa/%s_variance.csv'%city, 'w') as output:
        output.write('BLOCKGROUP FIP')
        for cl in sorted(classes.iterkeys()):
            output.write('\t%s'%cl)
        output.write('\n')
        for bg in rep:
            output.write(str(bg))
            for cat in sorted(rep[bg].iterkeys()):
                val, var = rep[bg][cat]
                output.write('\t%s'%var)
            output.write('\n')

