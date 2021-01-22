import requests
from bs4 import BeautifulSoup
import pandas as pd

store_id = 1

df = pd.DataFrame(columns = ['store_id','address','city','state','zip_code','phone_number'])

company_url = "https://locations.traderjoes.com/"
page = requests.get(company_url)
soup = BeautifulSoup(page.content, 'html.parser')
state_urls = soup.findAll("a", class_="ga_w2gi_lp")

for state in state_urls:
	state_url = state['href']
	print('Working on state:'+state_url)
	page = requests.get(state_url)
	soup = BeautifulSoup(page.content, 'html.parser')

	city_urls = soup.findAll("a", class_="ga_w2gi_lp")

	for city in city_urls:
		city_url = city['href']
		page = requests.get(city_url)
		soup = BeautifulSoup(page.content, 'html.parser')
		print("Working on city: " + city_url)

		stores = soup.findAll(class_="address-left")

		for store in stores:
			address = store.findAll("span")[1].text
			city = store.findAll("span")[2].text
			state = store.findAll("span")[3].text
			zip_code = store.findAll("span")[4].text
			phone_number = store.findAll("span")[6].text.strip()
			df = df.append({'store_id':store_id, 'address':address,'city':city,'state':state,'zip_code':zip_code,'phone_number':phone_number}, ignore_index = True)
			store_id = store_id + 1

df.to_csv('trader_joes.csv', index=False, header=True)


