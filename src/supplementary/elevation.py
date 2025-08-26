from ..config import parse
import os
import rasterio
import rasterio.mask
import numpy as np
from shapely.geometry import Point
# import geopandas as gpd
from pyproj import Transformer


def elevation_stats(dem_path, lat, lon, radius_m):
    """
    Calculate elevation statistics within a buffer around a lat/lon point.
    
    Parameters:
        dem_path (str): Path to DEM GeoTIFF.
        lat (float): Latitude of the point.
        lon (float): Longitude of the point.
        radius_m (float): Buffer radius in meters (assumes DEM CRS uses meters).
    
    Returns:
        dict: Dictionary with min, max, mean, std of elevation values.
    """
    # Open DEM
    with rasterio.open(dem_path) as src:
        dem_crs = src.crs
        nodata = src.nodata
        
        # Reproject point from WGS84 to DEM CRS
        transformer = Transformer.from_crs("EPSG:4326", dem_crs, always_xy=True)
        x, y = transformer.transform(lon, lat)
        
        # Create buffer geometry
        point = Point(x, y)
        buffer_geom = point.buffer(radius_m)
        
        # Mask the DEM with the buffer
        out_image, _ = rasterio.mask.mask(src, [buffer_geom], crop=True)
        data = out_image[0]
        
    # Remove nodata
    if nodata is not None:
        valid_data = data[data != nodata]
    else:
        valid_data = data[~np.isnan(data)]
    
    if valid_data.size == 0:
        return {
            "min": None,
            "max": None,
            "mean": None,
            "std": None
        }
    
    return {
        "min": float(np.min(valid_data)),
        "max": float(np.max(valid_data)),
        "mean": float(np.mean(valid_data)),
        "std": float(np.std(valid_data))
    }


def main():
    args = parse()
    data_directory = args["dem"]


if __name__ == "__main__":
    main()
    # dem_file = "your_dem.tif"  # Replace with your DEM file path
    # latitude = 35.123
    # longitude = -101.456
    # radius = 500  # meters
    
    # stats = elevation_stats(dem_file, latitude, longitude, radius)
    # print(f"Elevation stats within {radius} m of ({latitude}, {longitude}):")
    # print(stats)
