###
##
#

## Dependencies
import pandas as pd
import geopandas as gpd
from datetime import datetime
import pytz, argparse


## CLI
parser = argparse.ArgumentParser(description='Formats filtered locations points with time attributes')
parser.add_argument('-i', '--input', help='Filepath of filtered locations as .csv')
parser.add_argument('-o', '--output', help='Filepath of output .csv')

## Variables
args = parser.parse_args()
coords_f = args.input
output_f = args.output


## Functions
def parse_df_times(df):
    # Copy as to not mutate OG data
    copy_df = df.copy()
    # Parse Google UTC timestamp
    copy_df['parsed_timestamp'] = pd.to_datetime(copy_df['timestamp'], utc=True, infer_datetime_format=True)
    # Convert to Central Time
    copy_df['cst_timestamp'] = copy_df.parsed_timestamp.dt.tz_convert('America/Chicago')
    
    # Remove the verbose columns and rename to match
    slim_df = copy_df[['cst_timestamp', 'latitude', 'longitude']]
    slim_df.rename(columns={'cst_timestamp': 'timestamp'}, inplace=True)
    
    return slim_df

cst = pytz.timezone('America/Chicago')
years = {
    'freshman' : [datetime(year=2013, month=8, day=1, tzinfo=cst), datetime(year=2014, month=8, day=1, tzinfo=cst)],
    'sophomore': [datetime(year=2014, month=8, day=2, tzinfo=cst), datetime(year=2015, month=8, day=1, tzinfo=cst)],
    'junior'   : [datetime(year=2015, month=8, day=2, tzinfo=cst), datetime(year=2016, month=7, day=27, tzinfo=cst)],
    'senior'   : [datetime(year=2016, month=7, day=28, tzinfo=cst), datetime(year=2017, month=7, day=27, tzinfo=cst)],
    'postgrad' : [datetime(year=2017, month=7, day=28, tzinfo=cst), datetime(year=2018, month=10, day=1, tzinfo=cst)]
}

def assign_year(timestamp):
    for yr_obj in years.items():
        yr = yr_obj[0]
        start = yr_obj[1][0]
        end = yr_obj[1][1]
        
        if ((timestamp > start) and (timestamp < end)):
            return yr
    return 'none'

def is_weekend(day):
    return ((day == 'Saturday') or (day == 'Sunday'))

def is_business(timestamp):
    day = timestamp.weekday_name
    hour = timestamp.hour
    business_day = is_weekend(day) == False
    business_hrs = ((hour >= 7) and (hour < 19))
    return (business_day and business_hrs)

def format_df_cols(df):
    # Non-mutable
    copy_df = df.copy()
    
    # Add time attributes
    copy_df['weekday'] = df.timestamp.dt.day_name
    copy_df['dayhour'] = df.timestamp.dt.hour
    
    # Dimensions
    copy_df['weekend'] = copy_df['weekday'].apply(is_weekend)
    copy_df['year'] = copy_df['timestamp'].apply(assign_year)
    copy_df['business'] = copy_df['timestamp'].apply(is_business)
    
    return copy_df


## Script
coords_df = pd.read_csv(coords_f)
time_parsed_df = parse_df_times(coords_df)
df_attrs = format_df_cols(time_parsed_df)
df_attrs.to_csv(output_f, index=False)