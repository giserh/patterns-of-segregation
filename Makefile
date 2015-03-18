#
# Download and transform the data
#

# Decompress income data
data/income/us/household_incomes.csv:
	gzip -d $@



## Reconstitute 2000 census MSA
data/shp/msa/msa.shp: data/gz/tl_2010_us_county00.zip data/gz/99mfips.txt
	mkdir -p $(basename $@)
	# Extract MSA to county crosswalk
	# Merge counties to get msa shapefile	

data/gz/tl_2010_us_county00.zip:
	mkdir -p $(basename $@)
	curl "http://www2.census.gov/geo/tiger/TIGER2010/COUNTY/2000/$(notdir $@)" -o $@.download
	mv $@.download $@

data/gz/99mfips.txt:
	mkdir -p $(basename $@)
	curl "http://www.census.gov/population/metro/files/lists/historical/$(notdir $@)" -o $@.download
	mv $@.download $@



## Download census blocks



## Extract 




#
# Clean the folder of all (downloadable) data and outputs
#
clean:
	gzip -9 data/income/us/household_incomes.csv
	rm -r data/shp
	rm -r data/gz
	rm -r extr
	rm -r results
	rm -r figures
