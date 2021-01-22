import requests
from bs4 import BeautifulSoup
import pandas as pd

store_id = 1

df = pd.DataFrame(columns = ['store_id','address'])

state_urls = ["https://www.sprouts.com/stores/al/", 
"https://www.sprouts.com/stores/ut/",
"https://www.sprouts.com/stores/pa/",
"https://www.sprouts.com/stores/nj/",
"https://www.sprouts.com/stores/la/",
"https://www.sprouts.com/stores/de/",
"https://www.sprouts.com/stores/az/",
"https://www.sprouts.com/stores/fl/",
"https://www.sprouts.com/stores/md/",
"https://www.sprouts.com/stores/nm/",
"https://www.sprouts.com/stores/sc/",
"https://www.sprouts.com/stores/va/",
"https://www.sprouts.com/stores/ca/",
"https://www.sprouts.com/stores/ga/",
"https://www.sprouts.com/stores/mo/",
"https://www.sprouts.com/stores/nc/",
"https://www.sprouts.com/stores/tn/",
"https://www.sprouts.com/stores/wa/",
"https://www.sprouts.com/stores/co/",
"https://www.sprouts.com/stores/ka/",
"https://www.sprouts.com/stores/nv/",
"https://www.sprouts.com/stores/ok/",
"https://www.sprouts.com/stores/tx/"]

for state_url in state_urls:
	page = requests.get(state_url)
	soup = BeautifulSoup(page.content, 'html.parser')
	store_urls = soup.findAll("a", class_="no-external underline")

	for store in store_urls:
		store_url = store['href']
		print('Working on store:%s'%store_url)
		page = requests.get(store_url)
		soup = BeautifulSoup(page.content, 'html.parser')

		address = " ".join(soup.findAll(class_="store-address")[0].text.split())
		df = df.append({'store_id':store_id, 'address':address}, ignore_index = True)
		store_id = store_id + 1

df.to_csv('sprouts_market.csv', index=False, header=True)


