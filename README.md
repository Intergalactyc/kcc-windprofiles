# KCC wind profiles analysis
Author: Elliott Walker

Repository with code for study of wind profiles based on data at the 106-meter meteorological tower at Kirkwood Community College in Cedar Rapids, Iowa. The core package used in this analysis is [windprofiles](https://github.com/Intergalactyc/windprofiles).

This study is a joint work with Dr. Corey Markfort (University of Iowa) and Dr. Wei Zhang (Texas Tech University).

## Usage
Download or clone this repository onto your device. Make sure you have Python installed (any version 3.11+ should work, though this has only been strictly tested for version 3.12). Set up and activate a Python virtual environment (e.g. `python -m venv .venv` followed by `.venv/Scripts/activate`), and then install the necessary packages. Currently `windprofiles` is not available on PyPi, so you should download it [from the source GitHub repository](https://github.com/Intergalactyc/windprofiles) and install the package into your environment based on the instructions there. Then, back in this repository, you can use `pip install -r requirements.txt` to install the other dependencies.

As it currently stands, this analysis does not require any API keys (so nothing should need to be configured for `windprofiles`).

### Full analysis (from raw data)
This assumes that you have the raw meteorological tower data (seven files, `Boom1OneMin.csv` through `Boom7OneMin.csv`) in a directory somewhere on your local machine. Copy the `config_TEMPLATE.ini` file and rename the copy `config.ini`. In this file, change the data path to point to that directory.

Run `python src/primary/main.py` to perform the primary analysis. This will (re)generate basic data products in the `outputs` directory.

### Secondary analysis and figure generation (from processed data)
The contents of `outputs` are the data products generated in the primary analysis. Run `python src/secondary/main.py` for further analysis and figure generation. Figures will be placed in a `figs` directory (which will be created if it does not exist).
