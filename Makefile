# Variables
GOOGLE_TAKEOUT_ZIP = data/takeout-20181011T200640Z-001.zip


# Recipes
data/Takeout:
	unzip ${GOOGLE_TAKEOUT_ZIP} -d data
	rm data/Takeout/index.html
	mv data/Takeout/Location\ History/Location\ History.json data/Takeout
	rm -r data/Takeout/Location\ History/

data/Takeout/Location\ History\ Parsed.csv: data/Takeout
	python src/parse-points.py --input data/Takeout/Location\ History.json --output data/Takeout/Location\ History\ Parsed.csv