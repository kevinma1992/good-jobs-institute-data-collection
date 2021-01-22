import requests
from bs4 import BeautifulSoup
import pandas as pd

df = pd.DataFrame(columns = ['address','city','state','zip_code','phone_number'])

company_url = "https://locations.harristeeter.com/"
page = requests.get(company_url)
soup = BeautifulSoup(page.content, 'html.parser')
state_urls = soup.findAll(id="state_list")[0].findAll("a")

for state in state_urls:
	state_url = state['href']
	print('Working on state:'+state_url)
	page = requests.get(state_url)
	soup = BeautifulSoup(page.content, 'html.parser')

	city_urls =  soup.findAll(class_="city_item")

	for city in city_urls:
		city_url = city.findAll("a")[0]['href']
		print("Working on city: " + city_url)
		page = requests.get(city_url)
		soup = BeautifulSoup(page.content, 'html.parser')

		stores =  soup.findAll(id="locations")[0].findAll("a")

		for store in stores:
			store_address = store.text.strip()
			print("Working on store: " + store_address)

			store_list = store_address.split(",")
			address = store_list[0]
			city = store_list[1]
			state = store_list[2]
			zip_code = store_list[3]
			df = df.append({'address':address, 'city':city, 'state':state, 'zip_code':zip_code}, ignore_index = True)

df = df.drop_duplicates()
df.to_csv('harris_teeter.csv', index=False, header=True)


