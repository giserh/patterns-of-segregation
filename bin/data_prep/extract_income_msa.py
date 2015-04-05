"""extract_income_msa.py

Extract the household income per block group for each msa, using the
msa-to-county crosswalk.
"""
import csv


#
# Import data
#

## MSA to blockgroup 
bg_to_msa = {}
with open('data/crosswalks/msa_blockgroup.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        bg_to_msa[rows[1]] = rows[0]

## Income data at block-group level
incomes = {}
with open('data/income/us/household_incomes.csv', 'r') as source:
    reader = csv.reader(source, delimiter=',')
    reader.next()
    for rows in reader:
        incomes[rows[1]] = [int(i) for i in rows[7:]]



#
# Group by MSA
#
incomes_msa = {}
in_msa = 0
out_msa = 0
for bg in incomes:
    if bg in bg_to_msa:
        in_msa += 1
        msa = bg_to_msa[bg]
        if msa not in incomes_msa:
            incomes_msa[msa] = {}
        incomes_msa[msa][bg] = incomes[bg]
    else:
        out_msa += 1

print '%s blockgroups are inside MSAs'%in_msa
print '%s blockgroups are outside MSAs'%out_msa



#
# Save the data
#
for msa in incomes_msa:
    with open('data/income/msa/%s/income.csv'%msa, 'w') as output:
        output.write("BLOCKGROUP FIP\tLess than $10000\t$10000-$14999\t$15000-$19999\t$20000-$24999\t$25000-$29999\t$30000-$34999\t$35000-$39999\t$40000-$44999\t$45000-$49999\t$50000-$59999\t$60000-$74999\t$75000-$99999\t$100000-$124999\t$125000-$149999\t$150000-$199999\t$200000 or more\n")
        for bg in incomes_msa[msa]:
            output.write(str(bg)+'\t')
            output.write('\t'.join(map(str, incomes_msa[msa][bg])))
            output.write('\n')
