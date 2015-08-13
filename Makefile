all: download_data preprocess_data analysis figures


#######################
## DOWNLOAD THE DATA ##
#######################
download_data: data/income/us/household_incomes.csv data/crosswalks/msa_county.csv download_blockgroups


## Decompress income data
data/income/us/household_incomes.csv:
	gzip -d $@

## Reconstitute 2000 census MSA
data/crosswalks/msa_county.csv data/names/msa.csv: data/gz/99mfips.txt
	mkdir -p data/crosswalks
	mkdir -p data/names	
	python bin/data_prep/crosswalk_msa_county.py

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






#########################
## PREPROCESS THE DATA ##
#########################
preprocess_data: msa_income msa_blockgroups msa_adjacency blockgroups_surface city_size


## Extract msa to blockgroup crosswalk 
data/crosswalks/msa_blockgroup.csv: data/crosswalks/msa_county.csv data/income/us/household_incomes.csv
	mkdir -p $(dir $@) 
	python bin/data_prep/crosswalk_msa_blockgroup.py

## Extract income per msa
msa_income: data/crosswalks/msa_blockgroup.csv data/income/us/household_incomes.csv
	mkdir -p data/income/msa
	python bin/data_prep/extract_income_msa.py

## Extract msa block groups shape
msa_blockgroups: data/crosswalks/msa_blockgroup.csv download_blockgroups 
	mkdir -p data/shp/msa
	python bin/data_prep/extract_shape_msa.py	

# Extract, for each MSA, the adjacency list of the blockgroups it contains
msa_adjacency: 
	mkdir -p extr/adjacency_bg/msa
	python bin/data_prep/adjacency_blockgroups.py

## Compute the surface area of blockgroups
blockgroups_surface: data/names/msa.csv 
	mkdir -p data/surface_area/blockgroups
	python bin/data_prep/surface_blockgroups.py

## Compute the total number of households per city
city_size: 
	mkdir -p data/population/msa
	python bin/data_prep/msa_households.py




##############
## ANALYSIS ##
##############
analysis: categories_analysis find_classes_average classes_analysis



#
# Analysis on the original categories
#
categories_analysis: representation_categories neighbourhoods_categories exposure_msa_categories 


## Compute the representation of initial categories
representation_categories:
	mkdir -p extr/representation/categories/msa
	python bin/analysis/representation_categories.py

## Identify neighbourhoods of initial categories
neighbourhoods_categories:
	mkdir -p extr/neighbourhoods/categories/msa
	python bin/analysis/neighbourhoods_categories.py

## Compute exposure and isolation matrices
exposure_msa_categories:
	mkdir -p extr/exposure/categories/msa
	python bin/analysis/exposure_categories.py




#
# Find average classes across the US
#
find_classes_average: exposure_msa_average_categories find_msa_average_classes msa_average_linkage 
	
    
# Compute the exposure matrix averaged over all MSAs 
exposure_msa_average_categories:
	mkdir -p extr/exposure/categories/us/msa_average
	python bin/analysis/exposure_categories_us_average.py
	
# Find the classes from exposure matrix averaged over all MSAs
find_msa_average_classes:
	mkdir -p extr/classes/msa_average
	python bin/analysis/find_msa_average_classes.py

# Export the linkage matrix
msa_average_linkage:
	mkdir -p extr/linkage/msa_average
	python bin/analysis/msa_average_linkage.py




#
# Analysis of the cities once we have the classes
#
classes_analysis: representation_classes neighbourhoods_classes exposure_msa_classes exposure_msa_average_classes representation_percolation representation_density inter-urban_representation clustering neighbourhoods_content neighbourhoods_polycentrism neighbourhoods_numbers neighbourhoods_overlaps units_number


## Compute the representation of classes
representation_classes:
	mkdir -p extr/representation/classes/msa
	python bin/analysis/representation_classes.py

## Identify the areal units where the different classes are overrepresented
neighbourhoods_classes:
	mkdir -p extr/neighbourhoods/classes/msa
	python bin/analysis/neighbourhoods_classes.py

## Compute exposure and isolation matrices
exposure_msa_classes:
	mkdir -p extr/exposure/classes/msa
	python bin/analysis/exposure_classes.py

## Compute exposure between classes for average of msas
exposure_msa_average_classes:
	mkdir -p extr/exposure/classes/us/msa_average
	python bin/analysis/exposure_classes_us_average.py

## Compute the representation inside/outside density percolation clusters
representation_percolation:
	mkdir -p extr/representation/classes/density_percolation
	python bin/analysis/representation_density_percolation.py

## Compute the representation and population density
representation_density:
	mkdir -p extr/representation/classes/density
	python bin/analysis/representation_density.py

## See which classes are over- or underrepresented in cities compared to the US as a whole
inter-urban_representation:
	mkdir -p extr/representation/us
	python bin/analysis/city-level_representation.py

## Compute the clustering values
clustering:
	mkdir -p extr/clustering/classes
	python bin/analysis/clustering.py

## Compute the population contained in neighbourhoods
neighbourhoods_content:
	mkdir -p extr/neighbourhoods/content
	python bin/analysis/neighbourhoods_content.py

## Compute the relative size of the largest and second largest center
neighbourhoods_polycentrism:
	mkdir -p extr/neighbourhoods/polycentrism
	python bin/analysis/neighbourhoods_polycentrism.py

## Compute the number of units where classes are overrepresented
units_numbers:
	mkdir -p extr/units/numbers
	python bin/analysis/units_numbers.py

## Compute the number of clusters 
neighbourhoods_numbers:
	mkdir -p extr/neighbourhoods/numbers
	python bin/analysis/neighbourhoods_numbers.py

## Compute the respective overlap of neighbourhoods
neighbourhoods_overlap:
	mkdir -p extr/neighbourhoods/overlap
	python bin/analysis/neighbourhoods_overlap.py






##################
## PLOT FIGURES ##
##################
figures: paper_figures si_figures


#
# Figures in the paper
#
paper_figures: plot_neighbourhoods plot_inter-urban plot_percolation plot_clustering plot_polycentrism plot_centers plot_density

## Plot the Atlanta neighbourhoods
plot_neighbourhoods:
	mkdir -p figures/paper
	python bin/plot_neighbourhoods.py 0520

## Plot larger cities richer than smaller ones
plot_inter-urban:
	mkdir -p figures/paper
	python bin/plot_inter-urban.py

## Plot representation in low/high density areas of the various classes
plot_percolation:
	mkdir -p figures/paper
	python bin/plot_percolation.py

## Plot representation in low/high density areas of the various classes
plot_density:
	mkdir -p figures/paper
	python bin/plot_density.py

## Plot (normalised) clustering as a function of population
plot_clustering:
	mkdir -p figures/paper
	python bin/plot_clustering.py

## Plot the ratio of the size of the second largest neighbourhood over that of the largest
plot_polycentrism:
	mkdir -p figures/paper
	python bin/plot_polycentrism.py

## Plot the number of neighbourhoods as a function of the total population
plot_centers:
	mkdir -p figures/paper
	python bin/plot_centers.py



#
# SI figures
#
si_figures: plot_content plot_gini plot_scaling_classes plot_scaling_income
	
## Plot proportion of each class' population living in class neighbourhood
plot_content:
	mkdir -p figures/paper/si
	python bin/plot_neighbourhoods_content.py

## Plot the gini coefficient of the income distribution for all MSA
plot_gini:
	mkdir -p figures/paper/si
	python bin/plot_gini.py

## Plot the scaling of the number of households per class
plot_scaling_classes:
	mkdir -p figures/paper/si
	python bin/plot_scaling_classes.py

## Plot the scaling of the total income
plot_scaling_income:
	mkdir -p figures/paper/si
	python bin/plot_scaling_income.py

## Plot the number of overrepresented units versus the number of households
plot_overrepresented:
	mkdir -p figures/paper/si
	python bin/plot_overrepresented.py

	
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
