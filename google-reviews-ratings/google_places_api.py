import urllib.request
import json
import sys
import pandas as pd
import numpy as np
import re
import requests

def location_results(search_parameter,api_key):
	# Create URL
	url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=%s&inputtype=textquery&fields=place_id,name,formatted_address,rating,user_ratings_total&key=%s' % (search_parameter,api_key)

	# Make the http GET request for Google Maps API
	api_result = requests.get(url)

	return api_result.json()

def json_extract(obj, key):
	#Recursively fetch values from nested JSON.
	arr = []

	def extract(obj, arr, key):
		#Recursively search for values of key in JSON tree.
		if isinstance(obj, dict):
			for k, v in obj.items():
				if isinstance(v, (dict, list)):
					extract(v, arr, key)
				elif k == key:
					arr.append(v)
		elif isinstance(obj, list):
			for item in obj:
				extract(item, arr, key)
		return arr

	values = extract(obj, arr, key)
	return values

def main(args):
	stores_list = pd.read_csv(args[0])
	api_key = str(args[1])

	# clean up store locations list
	stores_list = stores_list.replace(np.nan, '', regex=True)
	stores_list['address'] = stores_list['address'].replace(',', '',regex=True)
	stores_list['address_consolidated'] = stores_list['store'] + ' ' + stores_list['address'] + ' ' + stores_list['city'] + ' ' + stores_list['state']
	stores_list['address_consolidated'] = stores_list['address_consolidated'].apply(str)

	# create dataframe to store all google reviews data
	df = pd.DataFrame(columns = ['store_id','google_place_id','store_name','formatted_address','rating','user_ratings_total'])

	for i in range(len(stores_list)):
		store_id = stores_list.loc[i,'store_id']
		print("Working on Store ID: %s" % store_id)

		search_parameter = stores_list.loc[i, 'address_consolidated']
		search_parameter = re.sub('\s\s+', ' ', search_parameter)
		search_parameter = '%20'.join(search_parameter.split(' '))
		result = location_results(search_parameter,api_key)
		print(result)

		# extract json and add to dataframe
		try:
			google_place_id = json_extract(result,'place_id')[0]
			store_name = json_extract(result,'name')[0]
			formatted_address = json_extract(result,'formatted_address')[0]
			rating = json_extract(result,'rating')[0]
			user_ratings_total = json_extract(result,'user_ratings_total')[0]

			df = df.append({'store_id':store_id,
				'google_place_id':google_place_id,
				'store_name':store_name,
				'formatted_address':formatted_address,
				'rating':rating,
				'user_ratings_total':user_ratings_total}, ignore_index = True) 
		except:
			print("No Results for: %s"%search_parameter)
			pass

	df.to_csv('google_api_results.csv', index=False, header=True)

if __name__ == "__main__":
   main(sys.argv[1:])
