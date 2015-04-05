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
        countysub = False
        if len(rows) > 2: countysub = rows[2] 
       
        if county not in county_to_msa:
            county_to_msa[county] = {}
        if msa not in county_to_msa[county]:
            county_to_msa[county][msa] = []
        if countysub:
            county_to_msa[county][msa].append(countysub)


## County Subdivision to blockgroup
cousub_to_bg = {}
with open('data/crosswalks/countysub_to_blockgroup.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        if rows[0] not in cousub_to_bg:
            cousub_to_bg[rows[0]] = []
        cousub_to_bg[rows[0]].append(rows[1])


## Places to blockgroup
place_to_bg = {}
with open('data/crosswalks/place_to_blockgroup.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        if rows[0] not in place_to_bg:
            place_to_bg[rows[0]] = []
        place_to_bg[rows[0]].append(rows[1])


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
        ## If County subdivisions involved, a county might be cut between
        ## different MSAs
        msas = county_to_msa[county].keys()
        for msa in msas:
            if msa not in msa_blockgroup:
                msa_blockgroup[msa] = [] 

            if len(county_to_msa[county][msa])>0:
                for sub in county_to_msa[county][msa]:
                    if sub in cousub_to_bg:
                        if bg in cousub_to_bg[sub]:
                            msa_blockgroup[msa].append(bg)
                    elif sub in place_to_bg:
                        if bg in place_to_bg[sub]:
                            msa_blockgroup[msa].append(bg)
                    else:
                        print sub
            else:
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
