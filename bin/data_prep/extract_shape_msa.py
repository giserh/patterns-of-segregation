"""extract_shape_msa.py

Output one shapefile per MSA containing all the blockgroups it contains
"""
import os
import csv
import fiona


#
# Import MSA to blockgroup crosswalk 
#
msa_to_bg = {}
with open('data/2000/crosswalks/msa_blockgroup.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        msa = rows[0]
        bg = rows[1]
        if msa not in msa_to_bg:
            msa_to_bg[msa] = []
        msa_to_bg[msa].append(bg)


#
# Perform the extraction
#
for msa in msa_to_bg:
    states = list(set([b[:2] for b in msa_to_bg[msa]]))

    ## Get all blockgroups
    all_bg = {}
    for st in states:
        with fiona.open('data/2000/shp/state/%s/blockgroups.shp'%st, 'r',
                'ESRI Shapefile') as source:
            source_crs = source.crs
            for f in source:
                all_bg[f['properties']['BKGPIDFP00']] = f['geometry']

    ## blockgroups within cbsa
    msa_bg = {bg: all_bg[bg] for bg in msa_to_bg[msa]}

    ## Save
    if not os.path.isdir('data/2000/shp/msa/%s'%msa):
        os.mkdir('data/2000/shp/msa/%s'%msa)

    schema = {'geometry': 'Polygon',
              'properties': {'BKGPIDFP00': 'str'}}
    with fiona.open('data/2000/shp/msa/%s/blockgroups.shp'%msa, 'w', 
            'ESRI Shapefile',
            crs = source_crs,
            schema = schema) as output:
        for bg in msa_bg:
            rec = {'geometry':msa_bg[bg], 'properties':{'BKGPIDFP00':bg}}
            output.write(rec)
