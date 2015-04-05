"""crosswalk_place_bg.py

Get the crosswalk between county subdivisions and blockgroups. Could not be
found online, so I am using geometrical methods.
"""
import fiona
from shapely.geometry import shape


## Only a few states are concerned
con_states = ['09', '23', '25', '33', '50', '44']

place_to_bg = {}
for state in con_states:
    print "Extracting crosswalk between places and block group for"
    print "state %s"%state
    #
    # Import data
    #
    ## County subdivisions
    place = {}
    with fiona.open('data/shp/%s/places.shp'%state, 'r', 'ESRI Shapefile') as source:
        for f in source:
            place[f['properties']['PLACEFP00']] = shape(f['geometry'])

    ## Block groups
    blockgroup = {}
    with fiona.open('data/shp/%s/blockgroups.shp'%state, 'r', 'ESRI Shapefile') as source:
        for f in source:
            blockgroup[f['properties']['BKGPIDFP00']] = shape(f['geometry'])


    #
    # Compute intersections
    #     Blockgroups may be contained in places and a simple
    #     intersects() will return the surrounding blockgroups as well. We thus
    #     need to check that the intersection is not a line.
    #
    for cs, cs_shape in place.iteritems():
        place_to_bg[cs] = []
        for bg, bg_shape in blockgroup.iteritems():
            if (bg_shape.intersects(cs_shape) and
                bg_shape.intersection(cs_shape).geom_type not in ['LineString',
                                                                'MultiLineString']):
                place_to_bg[cs].append(bg)



#
# Save the results
#
with open('data/crosswalks/place_blockgroup.csv', 'w') as output:
    output.write("PLACE FIP\tBLOCKGROUP FIP\n")
    for cs in place_to_bg:
        for bg in place_to_bg[cs]:
            output.write("%s\t%s\n"%(cs, bg))
