""" Iowa City Basemap

"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


class IC:
    def __init__(self, water_f, roads_f, building_f):
        self.df = self.combine_map_files(water_f, roads_f, building_f)
        self.layers = ['water', 'road', 'building']
        self.styles = {
            'water': {
                'alpha': 1,
                'linewidth': 0.25,
                'color': '#B0CCEA'
            },
            'road': {
                'alpha': 1,
                'linewidth': 0.625,
                'color': '#333333'
            },
            'building': {
                'alpha': 0.85,
                'linewidth': 0.25,
                'color': '#333333'
            }
        }
        self.colors = {
            'junior': 'tab:red',
            'senior': 'tab:blue',
            'postgrad': 'tab:green'
        }
        self.titles = {
            'junior': ' Junior Year Activity in Iowa City ',
            'senior': ' Senior Year Activity in Iowa City ',
            'postgrad': ' Postgraduate Activity in Iowa City '
        }

    def combine_map_files(self, water_f, roads_f, building_f):
        """ Combines mapping layers into one geodataframe. """
        # Read in data files
        water_df = gpd.read_file(water_f)
        roads_df = gpd.read_file(roads_f)
        build_df = gpd.read_file(building_f)

        # Assign classes to each layer
        water_df['class'], roads_df['class'], build_df['class'] = 'water', 'road', 'building'

        # Construct the geodataframe
        df_cols = ['class', 'geometry']
        df = pd.concat([water_df[df_cols], roads_df[df_cols], build_df[df_cols]])
        gdf = gpd.GeoDataFrame(df)

        return gdf

    def get_basemap(self):
        """ Returns a fig, axes for plotting against."""
        df = self.df

        # Create figure
        fig, axes = plt.subplots(1,
            figsize=(10, 10),
            facecolor='#eeeeee')

        # Set limits
        plt.xlim((-91.575, -91.52))
        plt.ylim((41.645, 41.68))

        # Map each layer
        for layer in self.layers:
            # Data subset
            layer_data = df[df['class'] == layer]

            # Style
            alpha = self.styles[layer]['alpha']
            linewidth = self.styles[layer]['linewidth']
            ec = self.styles[layer]['color']
            fc = ec if layer != 'road' else None

            # Plot
            layer_data.plot(ax=axes,
                            alpha=alpha,
                            linewidth=linewidth,
                            edgecolor=ec,
                            color=fc)

        # remove surrounding axes
        axes.set_axis_off()

        return fig, axes

    def plot_pts(self, df, yrs=['junior', 'senior', 'postgrad']):
        fig, axes = self.get_basemap()

        for yr in yrs:
            label = yr.capitalize()

            yr_df = df[df.year == yr]
            color = self.colors[yr]

            handle = yr_df.plot(ax=axes,
                        label=label,
                        marker='o',
                        markersize=10,
                        alpha=0.05,
                        facecolor=[color])

        # Set limits to account for pt limits extending beyond basemap
        plt.xlim((-91.575, -91.52))
        plt.ylim((41.645, 41.68))

        # Add text
        title = yrs[0] if len(yrs) == 1 else ''
        self.plot_text(axes, title)

        # Squarify
        self.plot_squarify(fig, axes)

        return fig, axes

    def plot_text(self, ax, yr=''):
        fc = '#F8F8F8'
        ec = '#DADADA'

        # add legend
        font_config = {
            'family': 'sans-serif',
            'size': 11
        }

        leg = ax.legend(loc='upper right',
            facecolor=fc,
            edgecolor=ec,
            markerscale=4,
            prop=font_config,
            labelspacing=0.75,
            borderpad=1,
            borderaxespad=0.5,
            handletextpad=1,
            fancybox=False,
            framealpha=1.0)
        
        for lh in leg.legendHandles: 
            lh.set_alpha(0.65)

        # add title
        plot_title = self.titles[yr] if yr != '' else 'Last 3 years of Iowa City Activity'

        ax.text(0, 0.97, plot_title,
          family='sans-serif',
          #weight='semibold',
          size=13,
          va='top',
          ha='left',
          transform=ax.transAxes,
          bbox={
              'boxstyle': 'square',
              'ec': ec,
              'fc': fc,
              'pad': 0.75
          }
          )

    def plot_squarify(self, f, ax):
        """ Resizes axis limits to 1:1 ratio, keeping center of map. """
        xlim, ylim = ax.get_xlim(), ax.get_ylim()
        xmed, ymed = (sum(xlim) / 2), (sum(ylim) / 2)

        xrange, yrange = xlim[1] - xlim[0], ylim[1] - ylim[0]        
        largest_range = max(xrange, yrange)
        half_lg_range = largest_range / 2
        
        new_xlim = [xmed - half_lg_range, xmed + half_lg_range]
        new_ylim = [ymed - half_lg_range, ymed + half_lg_range]
        
        ax.set_xlim(new_xlim)
        ax.set_ylim(new_ylim)