### parse-points.py
##  Ryan Larson
#   Parsing Latitude/Longitude, and timestamp information from Google Takeout Location History
#   Used with CLI interface

## Libs used in script
#  Used to make CLI args easier
import argparse
#  Used to read/write files and compute lat/lngs
import json, csv, math
#	 For timestamps
from datetime import datetime


## CLI Interface
parser = argparse.ArgumentParser(description='Convert Google Maps location history to csv file.')
parser.add_argument('-i', '--input', action="store", help='Filepath to location history .json file.', required=True)
parser.add_argument('-o', '--output', action="store", help='Filepath to write output .csv file.', required=True)

## Variables
args = parser.parse_args()
file = open(args.input)
data = json.load(file)
locations = data['locations']

## Parser
with open(args.output, 'w') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		filewriter.writerow(['timestamp', 'latitude', 'longitude', 'accuracy'])
		for l, location in enumerate(locations):
			timestamp = datetime.utcfromtimestamp(int(location['timestampMs']) / 1000)
			filewriter.writerow([timestamp, float(location['latitudeE7'])/math.pow(10, 7), float(location['longitudeE7'])/math.pow(10, 7)])

print('Done! Wrote ' + str(len(locations)) + ' points.')
