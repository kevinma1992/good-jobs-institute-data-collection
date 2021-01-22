# Google Reviews Ratings Scraper
## Authors: Kevin Ma, Souhail Halaby, Aparna Pande
 This folder contains code to scrape reviews data from Google Places API for every grocery store's location. The python script requires 
 - 1) your Google API Key, and 
 - 2) a csv of the locations that you want to pull reviews data on, and outputs a csv of every location's aggregate rating (on a scale of 1.0 to 5.0) and number of user ratings. 
 
 You can read more about the Google Places API documentation here: https://developers.google.com/places/web-service/details. To run the script, enter the following command into Terminal:

 python google_places_api.py [your_locations_csv_file] '[your_google_api_key]'