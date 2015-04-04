"""extract_income_msa.py

Extract the household income per block group for each msa, using the
msa-to-county crosswalk.
"""
import csv


#
# Import data
#

## MSA to counties crosswalk
county_to_msa = {}
with open('data/crosswalks/msa_county.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        county_to_msa[rows[1]] = rows[0]


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

