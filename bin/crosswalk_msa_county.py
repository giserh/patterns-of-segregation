"""build_2000_msa.py

Extract a usable crosswalk between 2000 Metropolitan areas and counties.
Reconstitute a shapefile for the 2000 MSAs from the counties.

Parameters
----------

99mfips.txt: Delineation of the 2000 Metropolitan Statistical Areas

Returns
-------

crosswalk_msa_county.csv
msa.shp
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
        county_fips = line[24:29].replace(" ", "")
        entity_fips = line[40:45].replace(" ", "")
        name = line[48:88].replace("\n", "")

        if pmsa_fips != "":
            if county_fips == "":
                msa[pmsa_fips] = {'name':name,
                                 'counties':[]}
            else:
                if entity_fips == "":
                    msa[pmsa_fips]['counties'].append(county_fips)
        else:
            if county_fips == "":
                msa[msa_fips] = {'name':name,
                                 'counties':[]}
            else:
                if entity_fips == "":
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
