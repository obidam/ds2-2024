# Projects guideline

## Github Procedure
- Fork this github repository to your own account
- Add a folder under ds2-2024/projects, name it with your group last names
- Work out your project codes/documentation and stage/push it to your folder on your fork
- Once finalized, create a pull request to the main branch

## Project 5: Ocean warming
 
*Description*: Because of the human driven intensification of the greenhouse effect, the ocean is warming. 
You can compute ocean heat content (OHC) and its trend with a regression (linear or not) for the entire ocean time series and extrapolate to the future, e.g. what is the expected ocean warming for the horizon 2100.

Instead of working globally, you can study the ocean warming locally. In that case, you can plot the local slopes of the different OHC time series and deduce where the ocean warming is moderate and where it is strong.

*Bibliography*:
[Last IPCC report on Ocean Heat Content changes](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter_09.pdf#page=35), [IPCC fig 9.6](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter_09.pdf#page=227), [Ocean warming](https://www.iucn.org/resources/issues-briefs/ocean-warming), [Global Ocean Heat and Salt Content: Seasonal, Yearly, and Pentadal Fields](https://www.ncei.noaa.gov/access/global-ocean-heat-content/), [European Indicator](https://marine.copernicus.eu/access-data/ocean-monitoring-indicators/global-ocean-heat-content-0-2000m)

*Data*:

[![Colab](https://img.shields.io/static/v1?label=Google&message=Open+data+with+Colab&color=blue&style=plastic&logo=google-colab)](https://colab.research.google.com/github/obidam/ds2-2024/blob/main/project/Eg_of_access_to_data_in_the_cloud.ipynb)

By default, you can use the [EN4 dataset](https://www.metoffice.gov.uk/hadobs/en4/) that is an interpolation of all available ocean observations (of temperature and salinity) onto a regular space/time grid.

This dataset can be accessed this way:
    
    from intake import open_catalog
    catalog_url = 'https://raw.githubusercontent.com/obidam/ds2-2024/main/ds2_data_catalog.yml'
    cat = open_catalog(catalog_url)
    ds = cat["en4"].to_dask()
    
or:

    fs = gcsfs.GCSFileSystem(project="alert-ground-261008")
    gcsmap = fs.get_mapper("opendata_bdo2020/EN.4.2.1.f.analysis.g10.zarr")
    ds = xr.open_zarr(gcsmap)
       
But, if you wish, you can try to use [climate model simulations data](https://www.wcrp-climate.org/wgcm-cmip/wgcm-cmip6) that are accessible here: [CMIP6 data](https://cloud.google.com/blog/products/data-analytics/new-climate-model-data-now-google-public-datasets).
       

## Project 6: Ocean warming contribution to Sea level rise
 
*Description*: Sea level increases because of changes in currents (dynamic effect) and because of ocean density changes (steric effect). Compute ocean density changes contribution to Sea level rises (thermosteric effect) and demonstrate that it is the driver of regional sea level change trends.
 
*Bibliography*:
[Overview](https://sealevel.nasa.gov/understanding-sea-level/overview), [Deep-ocean contribution to sea level and energy budget not detectable over the past decade](https://www.nature.com/articles/nclimate2387), [Last IPCC report on Sea Level changes](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter_09.pdf#page=55), [IPCC fig 9.12](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter_09.pdf#page=237)

*Data*: You can use the [EN4 dataset](https://www.metoffice.gov.uk/hadobs/en4/) that is an interpolation of all available ocean observations (of temperature and salinity) onto a regular space/time grid.

This dataset can be accessed this way:
    
    from intake import open_catalog
    catalog_url = 'https://raw.githubusercontent.com/obidam/ds2-2024/main/ds2_data_catalog.yml'
    cat = open_catalog(catalog_url)
    ds = cat["en4"].to_dask()

**Sea Level data** accessible on the catalog as well here:

    ds = cat["sea_surface_height"].to_dask()

You should also need GSW: https://teos-10.github.io/GSW-Python/

## Projects 7 and 8: Future Arctic sea ice change (Arctic) / the Atlantic Multidecadal Oscillation

*Description*: The Coupled Model Intercomparison Project is a framework within which a number of research centres produce predictions of the future evolution of the climate. Many climate centres use an ensemble approach, in which they produce several simulations for each scenario, using the same model configuration. By comparing these multiple simulations (“the ensemble"), we can estimate the probability that the climate will evolve in a certain way.

*Data*: Google host a part of these data via their Public Datasets programme (https://cloud.google.com/blog/products/data-analytics/new-climate-model-data-now-google-public-datasets).

This dataset can be accessed this way:

	df = pd.read_csv('https://storage.googleapis.com/cmip6/cmip6-zarr-consolidated-stores.csv')
	df_ssh = df.query("activity_id=='ScenarioMIP' & table_id == 'Omon' & variable_id == 'zos' & institution_id == 'IPSL'")
	gcs = gcsfs.GCSFileSystem(token='anon')
	zstore = df_ssh.zstore.values[-1]
	mapper = gcs.get_mapper(zstore)
	ds = xr.(mapper, consolidated=True)

Notebook with info on the CMIP experiments and example code for project 7, future Arctic sea ice: [![Colab](https://img.shields.io/static/v1?label=Google&message=Open+data+with+Colab&color=blue&style=plastic&logo=google-colab)](https://colab.research.google.com/github/obidam/ds2-2024/blob/main/project/Information_for_project_7%2C_Future_Arctic_Sea_Ice%2C_2024.ipynb)

Notebook with info on the CMIP experiments and example code for project 8, the Atlantic Multidecadal Oscillation: [![Colab](https://img.shields.io/static/v1?label=Google&message=Open+data+with+Colab&color=blue&style=plastic&logo=google-colab)](https://colab.research.google.com/github/obidam/ds2-2024/blob/main/project/Information_for_project_8%2C_the_Atlantic_Multidecadal_Oscillation.ipynb)
***
<img src="https://github.com/obidam/ds2-2024/raw/main/logo_isblue.jpg">
