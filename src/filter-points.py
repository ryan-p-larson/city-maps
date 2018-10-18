### filter-points.py
##  Ryan Larson
#   Filters Location points to just Johnson County GPS points. Run from repo
#   root with Make: make data/johnson-cnty-coords.csv

##  Dependencies
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import argparse

## CLI
parser = argparse.ArgumentParser(description='Filter location history to just Johnson County')
parser.add_argument('-l', '--locations', help='Filepath to "location history.csv"')
parser.add_argument('-c', '--counties', help='Filepath to Iowa counties shapefile')
parser.add_argument('-o', '--output', help='Filepath to write Johnson County')


## Functions
def convert_coords(coords_df):
    # Create a copy so we don't mutate original dataframe
    copy_df = coords_df.copy()
    
    # Zip the lat/lngs and create points from the ensuing list
    copy_df['coordinates'] = list(zip(copy_df.longitude, copy_df.latitude))
    copy_df['coordinates'] = copy_df['coordinates'].apply(Point)
    
    # Create and return a geodataframe
    gdf = gpd.GeoDataFrame(copy_df, geometry='coordinates')
    # Set projections
    gdf.crs = {'init': 'epsg:4326'}
    gdf = gdf.to_crs(epsg=4326)
    return gdf

def reproject_and_extract_counties(gdf):
    johnson = gdf[gdf.COUNTY == 'Johnson']
    proj_johnson = johnson.to_crs(epsg=4326)
    return proj_johnson

def join_and_filter_coords(county, coords):
    # Remove coords with less than 25ft of accuracy
    coords = coords[coords['accuracy'] <= 25]
    
    # keep all of the coords contained within the single county geodataframe
    cnty_coords = gpd.sjoin(county, coords, how='inner', op='contains')
    # Slim down the columns, as the join adds the county datum
    cnty_coords = cnty_coords[['timestamp', 'latitude', 'longitude', 'accuracy']]
    return cnty_coords


## Variables
args = parser.parse_args()
locations_f = args.locations
counties_f = args.counties
output_f = args.output

##  Location History
locations_df = pd.read_csv(locations_f)
coord_df = convert_coords(locations_df)

##  Iowa Counties
counties_df = gpd.read_file(counties_f)
johnson_cnty = reproject_and_extract_counties(counties_df)

## Merging Coords
johnson_cnty_coords = join_and_filter_coords(johnson_cnty, coord_df)
print ('Old coords:\t{}'.format(len(coord_df)))
print ('New coords:\t{}'.format(len(johnson_cnty_coords)))

johnson_cnty_coords.to_csv(output_f, index=False)