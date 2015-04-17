"""surface_blockgroups.py

Script to compute the surface area of blockgroups.
"""
import csv
from functools import partial

import fiona
import pyproj
from shapely.geometry import shape
from shapely.ops import transform



#
# Preparation
#

## Projection used to project polygons
project = partial(
    pyproj.transform,
    pyproj.Proj(init='epsg:4326'), # source coordinate system
    pyproj.Proj(init='epsg:3575')) # destination coordinate system


## Import list of MSA
msa = {}
with open('data/names/msa.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        msa[rows[0]] = rows[1]


for i,city in enumerate(msa):
    print "Surface area of blockgroups for %s (%s/%s)"%(msa[city], i+1, len(msa))

    ## Import blockgroups' surface area
    blocks = {}
    with fiona.open('data/shp/msa/%s/blockgroups.shp'%city, 'r', 'ESRI Shapefile') as source:
        for f in source:
            blocks[f['properties']['BKGPIDFP00']] = transform(project,
                                                        shape(f['geometry'])).area

    ## Save data
    with open('data/surface_area/blockgroups/%s_blockgroup_area.csv'%city, 'w') as output:
        output.write('Blockgroup FIP\tSurface area (m^2)\n')
        for bg in blocks:
            output.write('%s\t%s\n'%(bg, blocks[bg]))
