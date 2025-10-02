# KCC wind profiles analysis
Author: Elliott Walker (Texas Tech University)

Repository with code for study of wind profiles based on data at the 106-meter meteorological tower at Kirkwood Community College in Cedar Rapids, Iowa. The core package used in this analysis is [windprofiles](https://github.com/Intergalactyc/windprofiles).

This study is a joint work with Dr. Wei Zhang (Texas Tech University) and Dr. Corey Markfort (University of Iowa).

## Usage
Download or clone this repository onto your device. Make sure you have Python installed (any version 3.11+ should work, though this has only been strictly tested for version 3.12). Set up and activate a Python virtual environment (e.g. `python -m venv .venv` followed by `.venv/Scripts/activate`), and then install the necessary packages. Currently `windprofiles` is not available on PyPi, so you should download it [from the source GitHub repository](https://github.com/Intergalactyc/windprofiles) and install the package into your environment based on the instructions there. Then, back in this repository, you can use `pip install -r requirements.txt` to install the other dependencies.

As it currently stands, this analysis does not require any API keys (so nothing should need to be configured for `windprofiles`).

### Process: `process.py`
This assumes that you have the raw meteorological tower data (seven files, `Boom1OneMin.csv` through `Boom7OneMin.csv`) in a directory somewhere on your local machine. Copy the `config_TEMPLATE.ini` file and rename the copy `config.ini`. In this file, change the `data` path to point to that directory. You also need the corresponding CID airport weather data (included in this repository), change the `cid` path in the config file to point to this file.

Run `python src/process.py` to perform the processing. This will (re)generate basic data products in the `results/processed` directory.

### Analyze: `analyze.py`
The contents of `outputs` are the data products generated in the primary analysis. Run `python src/secondary/main.py` for further analysis and figure generation. Figures will be placed in a `figs` directory (which will be created if it does not exist).

Run `python src/analyze.py` to perform this analysis. This will (re)generate secondary data products in the `results/analysis` directory.

### Plot: `plot.py`
This will use the results from the Process and Analyze steps

Run `python src/plot.py` to generate figures. Figures will be in the `results/figures` directory.

## Data Sources
Met tower data: Kirkland Community College 106-meter meteorological tower

CID data: [Iowa Environmental Mesonet](https://mesonet.agron.iastate.edu/request/download.phtml?network=IA_ASOS), copy of specific data included in repository (`cid.csv`)

DEM lidar elevation raster: [USGS](https://apps.nationalmap.gov/downloader/#/?z=8&y=41.82408393116087&x=-93.54911804199266&basemap=usgs_topo&datasets=elevation-products-three-dep&layerIds=one-meter-dem) ([Iowa Geospatial Data Clearinghouse](https://geodata.iowa.gov/pages/lidar))
- [USGS_1M_15_x61y464_IA_EasternIA_2019_B19.tif](https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1m/Projects/IA_EasternIA_2019_B19/TIFF/USGS_1M_15_x61y464_IA_EasternIA_2019_B19.tif) ([metadata](https://www.sciencebase.gov/catalog/item/6369f1bad34ed907bf6a2934))
- [USGS_1M_15_x61y465_IA_EasternIA_2019_B19.tif](https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1m/Projects/IA_EasternIA_2019_B19/TIFF/USGS_1M_15_x61y465_IA_EasternIA_2019_B19.tif) ([metadata](https://www.sciencebase.gov/catalog/item/6369f1b9d34ed907bf6a2932))
