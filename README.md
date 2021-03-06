# GLCFS-Python-Data-Access
A library written in python to access public data from the Great Lakes Coastal Forecasting System from NOAA and parse it.

## About
This project is to make it easier for me to get data about the great lakes to see forecasts for things like waves.

All of this data is from the Great Lakes Forecasting System (https://www.glerl.noaa.gov/res/glcfs/) from the Great Lakes Environmental Research Laboratory, which is part of NOAA. Thank you to Greg Lang for helping me get set up with the data.

This project also uses Pandas and NumPy.

## Data
The data comes from this link on the GLERL site: https://www.glerl.noaa.gov/emf/glcfs/gridded_fields/

## Use
The maps directory has pickle files for pandas DataFrames for the coordinate encoding tables for all 5 great lakes, you can delete it if you want then use the create map functions in the Map Data class to make them all again or just the ones you need. The creation fetches them from the server but then pickles them for fast use and access in later runs.

* **To Get The Location:** Create a map data object using the Lake.LAKENAME enum to specify which lake. Then run decode coords on it to get the pandas series for the row with your data. That can then be passed to the static methods to extract the sequence number.

* **To Extract Information:** *This is a work in progress* Create a datafile object using the URL of the file you want. You can then set the column titles with the setDataframeTitles method. You can then use extractRows and the sequence number from the location to get a DataFrame of all the data for a single square of the lake with each date and time as the index and the predictions in the columns. Use the readme from GLERL to understand this data. 
