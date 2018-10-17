""" Coords.py
"""

import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt
from shapely.geometry import Point
from geoplot import kdeplot, pointplot


class Coords:
    def __init__(self, f):
        self.df = self.read_file(f)
        self.yrs = ['junior', 'senior', 'postgrad']
        self.colors = {
            'junior': 'tab:red',
            'senior': 'tab:blue',
            'postgrad': 'tab:green'
        }
        
    def read_file(self, f):
        # Read in
        df = pd.read_csv(f)
        df = self.group_pts(df)

        # Create geometry + geodataframe
        geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
        gdf = gpd.GeoDataFrame(df, crs={'init': 'epsg:4326'}, geometry=geometry)

        # Index by the bounding box of the IC map
        xmin, ymin, xmax, ymax = -91.47, 41.62, -91.58, 41.69
        gdf = gdf.cx[xmin:xmax, ymin:ymax]

        return gdf

    def group_pts(self, df):
        """ Returns a df of lat,lng coords groupbed by year. """
        grouped_coords = []

        for yr in df.year.unique().tolist():
            yr_df = df[df.year == yr]
            unique_yr = yr_df.groupby(['longitude', 'latitude', 'year'])\
                .size()\
                .reset_index()\
                .rename(columns={0: 'value'})
            
            grouped_coords.append(unique_yr)
        
        grouped_coords_df = pd.concat(grouped_coords)        
        return grouped_coords_df

    def get_yr(self, yr):
        return self.df[self.df['year'] == yr]

    def plot_dist(self, ax, sample=1000):
        for yr in self.yrs:
            yr_df = self.get_yr(yr)
            print (len(yr_df))

            color = self.colors[yr]

            kdeplot(df=yr_df,
                    ax=ax,
                    shade=True,
                    shade_lowest=False,
                    n_levels=7)

        plt.xlim((-91.575, -91.52))
        plt.ylim((41.645, 41.68))

    def plot_pts(self, ax, sample=1000):
        for yr in self.yrs:
            yr_df = self.get_yr(yr)
            color = self.colors[yr]

            yr_df.plot(ax=ax,
                        marker='o',
                        markersize=12,
                        alpha=0.1,
                        facecolor=[color]
            )

        plt.xlim((-91.575, -91.52))
        plt.ylim((41.645, 41.68))
            

