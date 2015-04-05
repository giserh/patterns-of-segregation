all: download_data preprocess_data



#
# Download and transform the data
#
download_data: data/income/us/household_incomes.csv data/crosswalks/msa_county.csv download_blockgroups download_countysubs download_places


## Decompress income data
data/income/us/household_incomes.csv:
	gzip -d $@



## Reconstitute 2000 census MSA
data/crosswalks/msa_county.csv data/names/msa.csv: data/gz/99mfips.txt
	mkdir -p data/crosswalks
	mkdir -p data/names	
	python2 bin/data_prep/crosswalk_msa_county.py

data/gz/99mfips.txt:
	mkdir -p $(dir $@)
	curl "http://www.census.gov/population/metro/files/lists/historical/$(notdir $@)" -o $@.download
	mv $@.download $@


## Download necessary county subdivisions:
data/gz/tl_2010_%_cousub00.zip:
	mkdir -p $(dir $@)
	curl 'http://www2.census.gov/geo/tiger/TIGER2010/COUSUB/2000/$(notdir $@)' -o $@.download
	mv $@.download $@

data/shp/state/%/countysub.shp: data/gz/tl_2010_%_cousub00.zip
	rm -rf $(basename $@)
	mkdir -p $(basename $@)
	unzip -d $(basename $@) $<
	for file in $(basename $@)/*; do chmod 644 $$file; mv $$file $(basename $@).$${file##*.}; done
	rmdir $(basename $@)
	touch $@


download_countysubs: data/shp/state/09/countysub.shp data/shp/state/23/countysub.shp data/shp/state/25/countysub.shp data/shp/state/33/countysub.shp data/shp/state/44/countysub.shp data/shp/state/50/countysub.shp


## Download necessary places
data/gz/tl_2010_%_place00.zip:
	mkdir -p $(dir $@)
	curl 'http://www2.census.gov/geo/tiger/TIGER2010/PLACE/2000/$(notdir $@)' -o $@.download
	mv $@.download $@

data/shp/state/%/places.shp: data/gz/tl_2010_%_place00.zip
	rm -rf $(basename $@)
	mkdir -p $(basename $@)
	unzip -d $(basename $@) $<
	for file in $(basename $@)/*; do chmod 644 $$file; mv $$file $(basename $@).$${file##*.}; done
	rmdir $(basename $@)
	touch $@

download_places: data/shp/state/09/places.shp data/shp/state/23/places.shp data/shp/state/25/places.shp data/shp/state/33/places.shp data/shp/state/44/places.shp data/shp/state/50/places.shp



## Download census block-groups
data/gz/tl_2010_%_bg00.zip:
	mkdir -p $(dir $@)
	curl 'http://www2.census.gov/geo/tiger/TIGER2010/BG/2000/$(notdir $@)' -o $@.download
	mv $@.download $@

data/shp/state/%/blockgroups.shp: data/gz/tl_2010_%_bg00.zip
	rm -rf $(basename $@)
	mkdir -p $(basename $@)
	unzip -d $(basename $@) $<
	for file in $(basename $@)/*; do chmod 644 $$file; mv $$file $(basename $@).$${file##*.}; done
	rmdir $(basename $@)
	touch $@

download_blockgroups: data/shp/state/01/blockgroups.shp data/shp/state/02/blockgroups.shp data/shp/state/04/blockgroups.shp data/shp/state/05/blockgroups.shp data/shp/state/06/blockgroups.shp data/shp/state/08/blockgroups.shp data/shp/state/09/blockgroups.shp data/shp/state/10/blockgroups.shp data/shp/state/11/blockgroups.shp data/shp/state/12/blockgroups.shp data/shp/state/13/blockgroups.shp data/shp/state/15/blockgroups.shp data/shp/state/16/blockgroups.shp data/shp/state/17/blockgroups.shp data/shp/state/18/blockgroups.shp data/shp/state/19/blockgroups.shp data/shp/state/20/blockgroups.shp data/shp/state/21/blockgroups.shp data/shp/state/22/blockgroups.shp data/shp/state/23/blockgroups.shp data/shp/state/24/blockgroups.shp data/shp/state/25/blockgroups.shp data/shp/state/26/blockgroups.shp data/shp/state/27/blockgroups.shp data/shp/state/28/blockgroups.shp data/shp/state/29/blockgroups.shp data/shp/state/30/blockgroups.shp data/shp/state/31/blockgroups.shp data/shp/state/32/blockgroups.shp data/shp/state/33/blockgroups.shp data/shp/state/34/blockgroups.shp data/shp/state/35/blockgroups.shp data/shp/state/36/blockgroups.shp data/shp/state/37/blockgroups.shp data/shp/state/38/blockgroups.shp data/shp/state/39/blockgroups.shp data/shp/state/40/blockgroups.shp data/shp/state/41/blockgroups.shp data/shp/state/42/blockgroups.shp data/shp/state/44/blockgroups.shp data/shp/state/45/blockgroups.shp data/shp/state/46/blockgroups.shp data/shp/state/47/blockgroups.shp data/shp/state/48/blockgroups.shp data/shp/state/49/blockgroups.shp data/shp/state/50/blockgroups.shp data/shp/state/51/blockgroups.shp data/shp/state/53/blockgroups.shp data/shp/state/54/blockgroups.shp data/shp/state/55/blockgroups.shp data/shp/state/56/blockgroups.shp data/shp/state/60/blockgroups.shp data/shp/state/66/blockgroups.shp data/shp/state/69/blockgroups.shp data/shp/state/72/blockgroups.shp data/shp/state/78/blockgroups.shp 





#
# Pre-process the data
#
preprocess_data: msa_income msa_blockgroups


## Extract county subdivisions to blockgroup crosswalk
data/crosswalks/countysub_blockgroup.csv:
	mkdir -p $(dir $@) 
	python2 bin/data_prep/crosswalk_countysub_blockgroup.py

## Extract places to blockgroup crosswalk
data/crosswalks/place_blockgroup.csv:
	mkdir -p $(dir $@) 
	python2 bin/data_prep/crosswalk_place_blockgroup.py

## Extract msa to blockgroup crosswalk 
data/crosswalks/msa_blockgroup.csv: data/crosswalks/countysub_blockgroup.csv data/crosswalks/place_blockgroup.csv
	mkdir -p $(dir $@) 
	python2 bin/data_prep/crosswalk_msa_blockgroup.py

## Extract income per msa
msa_income: data/crosswalks/msa_blockgroup.csv data/income/us/household_incomes.csv
	python2 bin/data_prep/extract_income_msa.py

## Extract msa block groups shape
msa_blockgroups: data/crosswalks/msa_blockgroup.csv download_blockgroups 
	mkdir -p data/shp/msa
	python2 bin/data_prep/extract_shape_msa.py	

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
	rm -r data/names
