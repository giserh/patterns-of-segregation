"""plot_neighbourhoods.py

Plot the neighbourhoods of all classes for the city specified as an input with the following color codes
* Black: where the class is over-represented (with 99% CI)
* Light grey: where the class is 'normally' represented
* White: where the class is under-represented
"""
import sys
import math
import csv
import fiona
from descartes import PolygonPatch
from shapely.geometry import shape
from matplotlib import pylab as plt


#
# Parameters
#

## Read city from input
city = sys.argv[1]

## Colors
colours = {'over': 'black',
        'norm': 'grey',
        'under': 'white'}




#
# Import data
#

## Blockgroups borders
blocks = {}
with fiona.open('data/shp/msa/%s/blockgroups.shp'%city, 'r', 'ESRI Shapefile') as source:
    for f in source:
        blocks[f['properties']['BKGPIDFP00']] = shape(f['geometry'])

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

## Representation values
rep_vals = {}
with open('extr/representation/classes/msa/%s_values.csv'%city, 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    classes_list = reader.next()[1:]
    for rows in reader:
        rep_vals[rows[0]] = {cl:float(r) for cl,r in zip(classes_list,
                                                        rows[1:])}

## Representation variance
rep_var = {}
with open('extr/representation/classes/msa/%s_variance.csv'%city, 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    classes_list = reader.next()[1:]
    for rows in reader:
        rep_var[rows[0]] = {cl:float(r) for cl,r in zip(classes_list,
                                                        rows[1:])}

        
#
# Transform representation values and variance into list of areal units
#
representation = {cl:{} for cl in classes} # cl:{bckgp:over, under, or norm}
for bg in rep_vals:
    for cl in classes:
        rep = rep_vals[bg][cl]-1
        std = math.sqrt(rep_var[bg][cl])

        ## if wihin 2.57 sigma or nan, mark as normal
        if abs(rep) <= 2.57*std or math.isnan(rep):
            representation[cl][bg] = 'norm'
        ## else it is over-represented or under
        else:
            if rep < 0:
                representation[cl][bg] = 'under'
            else: 
                representation[cl][bg] = 'over'


#
# Plot 
#

fig = plt.figure()
for i,cl in enumerate(classes):
    if i==0:
        ax = fig.add_subplot(1,len(classes),i+1)
    else:
        ax = fig.add_subplot(1,len(classes),i+1, sharex=ax, sharey=ax)
    for bg in representation[cl]:
        color = colours[representation[cl][bg]]
        if blocks[bg].geom_type=="Polygon":
            patch = PolygonPatch(blocks[bg], fc=color, ec='None', alpha=1, zorder=1)
            ax.add_patch(patch)
        else:
            for t in blocks[bg]:
                patch = PolygonPatch(t, fc=color, ec='None', alpha=1, zorder=1)
                ax.add_patch(patch)

    ax.relim()
    ax.axis('off')
    ax.autoscale_view(True,True,True)
    ax.set_title(r"$%s$"%cl,fontsize=25)

#plt.savefig('figures/paper/%s_neighbourhoods.png'%msa[city].replace(" ","").replace(",", ""),
#           bbox_inches='tight')
plt.show()
