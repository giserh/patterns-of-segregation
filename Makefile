all: data download_blockgroups

#
# Download and transform the data
#

data: data/income/us/household_incomes.csv data/crosswalks/msa_county.csv


## Decompress income data
data/income/us/household_incomes.csv:
	gzip -d $@



## Reconstitute 2000 census MSA
data/crosswalks/msa_county.csv: data/gz/99mfips.txt
	mkdir -p $(dir $@)
	python2 bin/crosswalk_msa_county.py

data/gz/99mfips.txt:
	mkdir -p $(dir $@)
	curl "http://www.census.gov/population/metro/files/lists/historical/$(notdir $@)" -o $@.download
	mv $@.download $@



## Download census block-groups
data/gz/tl_2010_%_bg00.zip:
	mkdir -p $(dir $@)
	curl 'http://www2.census.gov/geo/tiger/TIGER2010/BG/2000/$(notdir $@)' -o $@.download
	mv $@.download $@

data/shp/%/blockgroups.shp: data/gz/tl_2010_%_bg00.zip
	rm -rf $(basename $@)
	mkdir -p $(basename $@)
	unzip -d $(basename $@) $<
	for file in $(basename $@)/*; do chmod 644 $$file; mv $$file $(basename $@).$${file##*.}; done
	rmdir $(basename $@)
	touch $@

download_blockgroups: data/shp/01/blockgroups.shp data/shp/02/blockgroups.shp data/shp/04/blockgroups.shp data/shp/05/blockgroups.shp data/shp/06/blockgroups.shp data/shp/08/blockgroups.shp data/shp/09/blockgroups.shp data/shp/10/blockgroups.shp data/shp/11/blockgroups.shp data/shp/12/blockgroups.shp data/shp/13/blockgroups.shp data/shp/15/blockgroups.shp data/shp/16/blockgroups.shp data/shp/17/blockgroups.shp data/shp/18/blockgroups.shp data/shp/19/blockgroups.shp data/shp/20/blockgroups.shp data/shp/21/blockgroups.shp data/shp/22/blockgroups.shp data/shp/23/blockgroups.shp data/shp/24/blockgroups.shp data/shp/25/blockgroups.shp data/shp/26/blockgroups.shp data/shp/27/blockgroups.shp data/shp/28/blockgroups.shp data/shp/29/blockgroups.shp data/shp/30/blockgroups.shp data/shp/31/blockgroups.shp data/shp/32/blockgroups.shp data/shp/33/blockgroups.shp data/shp/34/blockgroups.shp data/shp/35/blockgroups.shp data/shp/36/blockgroups.shp data/shp/37/blockgroups.shp data/shp/38/blockgroups.shp data/shp/39/blockgroups.shp data/shp/40/blockgroups.shp data/shp/41/blockgroups.shp data/shp/42/blockgroups.shp data/shp/44/blockgroups.shp data/shp/45/blockgroups.shp data/shp/46/blockgroups.shp data/shp/47/blockgroups.shp data/shp/48/blockgroups.shp data/shp/49/blockgroups.shp data/shp/50/blockgroups.shp data/shp/51/blockgroups.shp data/shp/53/blockgroups.shp data/shp/54/blockgroups.shp data/shp/55/blockgroups.shp data/shp/56/blockgroups.shp data/shp/60/blockgroups.shp data/shp/64/blockgroups.shp data/shp/66/blockgroups.shp data/shp/68/blockgroups.shp data/shp/69/blockgroups.shp data/shp/70/blockgroups.shp data/shp/72/blockgroups.shp data/shp/74/blockgroups.shp data/shp/78/blockgroups.shp 

#
#
# Pre-process the data
#

## Extract income by msa

## Extract msa block groups


#
#
#


#
# Clean the folder of all (downloadable) data and outputs
#
clean:
	gzip -9 data/income/us/household_incomes.csv
	rm -r data/gz
	rm -r data/crosswalks
	rm -r data/shp
