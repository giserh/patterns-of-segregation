"""build_2000_msa.py

Extract a usable crosswalk between 2000 Metropolitan areas and counties.
Reconstitute a shapefile for the 2000 MSAs from the counties.

Parameters
----------

99mfips.txt: Delineation of the 2000 Metropolitan Statistical Areas

Returns
-------

crosswalk_msa_county.csv
msa.csv: names of MSAs
"""

#
# Parse the delineations provided by the OMB
#
begin_file = 22
end_file = 2173
msa = {}
with open('data/gz/99mfips.txt', 'r') as source:
    line = source.readline()
    l = 1
    while line:

        ## Skip the non-data lines
        if l < begin_file or l > end_file or line == "\n":
            line = source.readline()
            l+=1
            continue

        ## Read the data
        msa_fips = line[0:4].replace(" ", "")
        pmsa_fips = line[8:12].replace(" ", "")
        county_fips = line[24:29].replace(" ", "") # County
        countysub_fips = line[40:45].replace(" ", "") # County subdivision
        name = line[48:].replace("\n", "").lstrip().replace(" CMSA", "")

        if county_fips == "" and pmsa_fips == "":
            msa[msa_fips] = {'name':name.replace(" MSA", ""),
                            'counties':[]}
        else:
            if countysub_fips == "" and county_fips != "":
                if county_fips not in msa[msa_fips]['counties']:
                    msa[msa_fips]['counties'].append(county_fips) 

        ## Iterate
        line = source.readline()
        l+=1


## Remove the (empty) CMSA
msa = {fip:data for fip, data in msa.iteritems()
                if len(data['counties']) > 0}


#
# Save the crosswalk
#
with open("data/crosswalks/msa_county.csv", "w") as output:
    output.write("MSA FIPS CODE\tCOUNTY FIPS CODE\n")
    for city in msa:
        for county in msa[city]['counties']:
                output.write("%s\t%s\n"%(city, county))


#
# Save the names
#
with open("data/names/msa.csv", "w") as output:
    output.write("MSA FIPS CODE\t Name\n")
    for city in msa:
        output.write("%s\t%s\n"%(city, msa[city]['name']))
