all: download_data preprocess_data analysis



#
# Download and transform the data
#
download_data: data/income/us/household_incomes.csv data/crosswalks/msa_county.csv download_blockgroups


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
preprocess_data: msa_income msa_blockgroups msa_adjacency


## Extract msa to blockgroup crosswalk 
data/crosswalks/msa_blockgroup.csv: data/crosswalks/msa_county.csv
	mkdir -p $(dir $@) 
	python2 bin/data_prep/crosswalk_msa_blockgroup.py

## Extract income per msa
msa_income: data/crosswalks/msa_blockgroup.csv data/income/us/household_incomes.csv
	mkdir -p data/income/msa
	python2 bin/data_prep/extract_income_msa.py

## Extract msa block groups shape
msa_blockgroups: data/crosswalks/msa_blockgroup.csv download_blockgroups 
	mkdir -p data/shp/msa
	python2 bin/data_prep/extract_shape_msa.py	

msa_adjacency: 
	mkdir -p extr/adjacency_bg/msa
	python2 bin/data_prep/adjacency_blockgroups.py




#
# Perform the analysis
#
analysis: representation_categories neighbourhoods_categories exposure_msa_categories classes_average representation_classes neighbourhoods_classes exposure_msa_classes 

## Compute the representation of initial categories
representation_categories:
	mkdir -p extr/representation/categories/msa
	python2 bin/representation_categories.py

## Identify neighbourhoods of initial categories
neighbourhoods_categories:
	mkdir -p extr/neighbourhoods/categories/msa
	python2 bin/neighbourhoods_categories.py

## Compute exposure and isolation matrices
exposure_msa_categories:
	mkdir -p extr/exposure/categories/msa
	python2 bin/exposure_categories.py



## Find classes for the average MSA exposure matrix
classes_average: exposure_msa_average find_msa_average_classes
	
# Compute the exposure matrix averaged over all MSAs 
exposure_msa_average:
	mkdir -p extr/exposure/categories/us/msa_average
	python2 bin/exposure_us_average.py
	
# Find the classes from exposure matrix averaged over all MSAs
find_msa_average_classes:
	mkdir -p extr/classes/msa_average
	python2 bin/find_msa_average_classes.py



## Compute the representation of classes
representation_classes:
	mkdir -p extr/representation/classes/msa
	python2 bin/representation_classes.py

## Identify neighbourhoods of the different classes
neighbourhoods_classes:
	mkdir -p extr/neighbourhoods/classes/msa
	python2 bin/neighbourhoods_classes.py

## Compute exposure and isolation matrices
exposure_msa_classes:
	mkdir -p extr/exposure/classes/msa
	python2 bin/exposure_classes.py


#
# Plot the paper's figures
#
figures: plot_neighbourhoods

## Plot the hierarchical tree corresponding to class emergence

## Plot the Atlanta neighbourhoods
plot_neighbourhoods:
	mkdir -p figures/paper
	python2 bin/plot_neighbourhoods.py 0520

## Plot larger cities richer than smaller ones

## Plot representation in low/high density areas of the various classes

## Plot (normalised) clutering as a function of population

## Plot proportion of each class' population living in class neighbourhood

## Plot the ratio of the size of the second largest neighbourhood over that of the largest

## Plot the number of neighbourhoods as a function of the total population

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
	rm -r data/income/msa
	rm -r extr
