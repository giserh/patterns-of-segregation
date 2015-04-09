"""crosswalk_msa_blockgroup.py

Extract the crosswalk between msa and blockgroups
"""
import os
import csv
import collections

#
# Import data
#

## MSA to counties crosswalk
# county_to_msa = {county: {msa: [cousub ids]}
county_to_msa = {}
with open('data/crosswalks/msa_county.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        county = rows[1]
        msa = rows[0]
        county_to_msa[county] = msa


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
msa_blockgroup = {}
for bg in incomes:
    county = bg[:5]
    if county in county_to_msa:
        msa = county_to_msa[county]
        if msa not in msa_blockgroup:
            msa_blockgroup[msa] = []
        msa_blockgroup[msa].append(bg)




#
# Save the crosswalk 
#
with open('data/crosswalks/msa_blockgroup.csv', 'w') as output:
    output.write('MSA FIP\tBLOCKGROUP FIP\n')
    for msa in msa_blockgroup:
        ## Remove duplicates
        bgs = list(set(msa_blockgroup[msa]))
        for bg in bgs:
            output.write('%s\t%s\n'%(msa, bg))
