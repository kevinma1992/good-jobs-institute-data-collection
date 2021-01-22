import requests
from bs4 import BeautifulSoup
import pandas as pd

store_id = 1

df1 = pd.DataFrame(columns = ['store_id','store_url'])

df2 = pd.DataFrame(columns = ['store_id','address','city','state','zip_code','phone_number'])

base_url = "https://savealot.com"

company_url = "https://savealot.com/grocery-stores/"
page = requests.get(company_url)
soup = BeautifulSoup(page.content, 'html.parser')
state_urls = soup.findAll("ul")[1].findAll("a")

for state in state_urls:
	state_url = state['href']
	print('Working on state:'+state_url)
	page = requests.get(base_url+state_url)
	soup = BeautifulSoup(page.content, 'html.parser')

	city_urls = soup.findAll("ul")[1].findAll("a")

	for city in city_urls:
		city_url = city['href']
		page = requests.get(base_url+city_url)
		soup = BeautifulSoup(page.content, 'html.parser')
		print("Working on city: " + city_url)

		try:
			store_urls = soup.findAll("ul")[1].findAll("a")

			for store in store_urls:
				store_url = store['href']
				df1 = df1.append({'store_id':store_id, 'store_url':store_url}, ignore_index = True)
				store_id = store_id + 1
		except:
			print("Skipped city: %s"%city_url)
			pass

for url in df1['store_url']:
	print("working on #%d: %s"%(store_id,url))
	try:
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		address = " ".join(soup.findAll(class_="address")[0].text.split())
		df2 = df2.append({'store_id':store_id, 'address':address}, ignore_index = True)
		store_id = store_id + 1
	except:
		print("Skipping store: %s"%url)
		pass

df2.to_csv('savealot.csv', index=False, header=True)


