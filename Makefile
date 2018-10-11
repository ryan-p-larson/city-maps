# Variables
GOOGLE_TAKEOUT_ZIP = data/takeout-20181011T200640Z-001.zip
IA_COUNTY_URL = https://iowageodata.s3.amazonaws.com/boundaries/county.zip

### Recipes
## Google Takeout Data
data/Takeout:
	unzip ${GOOGLE_TAKEOUT_ZIP} -d data
	rm data/Takeout/index.html
	mv data/Takeout/Location\ History/Location\ History.json data/Takeout
	rm -r data/Takeout/Location\ History/

# Parsing just lat/lng/timestamps
data/Takeout/Location\ History\ Parsed.csv: data/Takeout
	python src/parse-points.py --input data/Takeout/Location\ History.json --output data/Takeout/Location\ History\ Parsed.csv


## Iowa Counties
data/counties:
	mkdir data/counties

data/counties/county.zip: data/counties
	curl ${IA_COUNTY_URL} --output $@
	unzip $@ -d $<
	rm $@