from config import parse
from windprofiles.gis.raster import Raster
from definitions import LOCATION, TOWER_HEIGHT, TERRAIN_WINDOW_WIDTH_DEGREES
import os

DEM_FILENAMES = ["USGS_1M_15_x61y465_IA_EasternIA_2019_B19.tif", "USGS_1M_15_x61y464_IA_EasternIA_2019_B19.tif"]

# Angles for terrain classifications, in degrees CCW of E (rather than CW of N, so the centers effectively swap)
OPEN_START = 315 - TERRAIN_WINDOW_WIDTH_DEGREES/2
OPEN_END = 315 + TERRAIN_WINDOW_WIDTH_DEGREES/2
COMPLEX_START = 135 - TERRAIN_WINDOW_WIDTH_DEGREES/2
COMPLEX_END = 135 + TERRAIN_WINDOW_WIDTH_DEGREES/2

def elevation_stats():
    args = parse()
    data_directory = args["dem"]
    dem_filepaths = [os.path.join(data_directory, f) for f in DEM_FILENAMES]
    dem = Raster.from_files(dem_filepaths)

    circle_1d3x = dem.circular_region_around(*LOCATION.coords, radius=1.3*TOWER_HEIGHT)
    stats_circle = dem.stats_in_region(circle_1d3x)
    print(stats_circle)

    open_terrain_5x = dem.circular_region_around(*LOCATION.coords, radius=5*TOWER_HEIGHT, sector_start=OPEN_START, sector_end=OPEN_END)
    stats_open_5x = dem.stats_in_region(open_terrain_5x)
    print(stats_open_5x)

    complex_terrain_5x = dem.circular_region_around(*LOCATION.coords, radius=5*TOWER_HEIGHT, sector_start=COMPLEX_START, sector_end=OPEN_END)
    stats_complex_5x = dem.stats_in_region(complex_terrain_5x)
    print(stats_complex_5x)

    # Next want to fit plane in the 1d3x circle, determine its angle, and find max deviations from that plane in the different sectors at 5, 10, 20x radius
    # https://dlbargh.ir/mbayat/46.pdf

if __name__ == "__main__":
    elevation_stats()
