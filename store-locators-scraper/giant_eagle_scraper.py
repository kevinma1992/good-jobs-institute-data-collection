import requests
from bs4 import BeautifulSoup
import pandas as pd

store_id = 1

df = pd.DataFrame(columns = ['store_id','address','city','state','zip_code'])

state_urls = ["https://grocery.gianteagle.com/pd/stores/OH", 
"https://grocery.gianteagle.com/pd/stores/PA",
"https://grocery.gianteagle.com/pd/stores/WV",
"https://grocery.gianteagle.com/pd/stores/IN"]

for state_url in state_urls:
	page = requests.get(state_url)
	soup = BeautifulSoup(page.content, 'html.parser')
	store_urls = soup.findAll(id="storeName")

	for store in store_urls:
		store_url = store.findAll("a")[0]['href']
		print('Working on store:%s'%store_url)
		page = requests.get(store_url)
		soup = BeautifulSoup(page.content, 'html.parser')

		address = soup.findAll(itemprop="streetAddress")[0].text
		city = soup.findAll(itemprop="addressLocality")[0].text
		state = soup.findAll(itemprop="addressRegion")[0].text
		zip_code = soup.findAll(itemprop="postalCode")[0].text

		df = df.append({'store_id':store_id, 'address':address,'city':city,'state':state,'zip_code':zip_code}, ignore_index = True)
		store_id = store_id + 1

df.to_csv('giant_eagle.csv', index=False, header=True)


