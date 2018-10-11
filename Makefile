# Variables
GOOGLE_TAKEOUT_ZIP = data/takeout-20181011T200640Z-001.zip
GOOGLE_TAKEOUT_JSON = data/Takeout/Location\ History.json
GOOGLE_TAKEOUT_PARSED = data/Takeout/Location\ History\ Parsed.csv

IA_COUNTY_URL = https://iowageodata.s3.amazonaws.com/boundaries/county.zip
IA_COUNTY_ZIP = data/counties/county.zip
IA_COUNTY_SHP = data/counties/county.shp

JOHNSON_COUNTY_CSV = data/johnson-cnty-coords.csv


### Recipes
## Google Takeout Data
data/Takeout: ${GOOGLE_TAKEOUT_ZIP}
	unzip ${GOOGLE_TAKEOUT_ZIP} -d data
	rm data/Takeout/index.html
	mv data/Takeout/Location\ History/Location\ History.json data/Takeout
	rm -r data/Takeout/Location\ History/

# Parsing just lat/lng/timestamps
${GOOGLE_TAKEOUT_PARSED}: data/Takeout
	python src/parse-points --input ${GOOGLE_TAKEOUT_JSON} --output $@

## Iowa Counties
data/counties:
	mkdir data/counties

${IA_COUNTY_ZIP}: data/counties
	curl ${IA_COUNTY_URL} --output $@

${IA_COUNTY_SHP}: ${IA_COUNTY_ZIP}
	unzip $< -d data/counties


## Johnson County Location History
${JOHNSON_COUNTY_CSV}: ${IA_COUNTY_SHP} ${GOOGLE_TAKEOUT_PARSED} 
	python src/filter-points.py \
	--locations ${GOOGLE_TAKEOUT_PARSED} \
	--counties ${IA_COUNTY_SHP} \
	--output $@