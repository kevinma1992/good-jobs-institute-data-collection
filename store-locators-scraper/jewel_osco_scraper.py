import requests
from bs4 import BeautifulSoup
import pandas as pd

df = pd.DataFrame(columns = ['address','city','state','zip_code','phone_number'])

base_url = "https://local.jewelosco.com/"

company_url = "https://local.jewelosco.com/"
page = requests.get(company_url)
soup = BeautifulSoup(page.content, 'html.parser')
state_urls = soup.findAll("a",class_="Directory-listLink")

for state in state_urls:
	state_url = state['href']
	print('Working on state:'+state_url)
	page = requests.get(base_url+state_url)
	soup = BeautifulSoup(page.content, 'html.parser')

	store_urls = soup.findAll("a", class_= "Directory-listLink")

	for store in store_urls:
		store_url = store['href']

		page = requests.get(base_url+store_url)
		soup = BeautifulSoup(page.content, 'html.parser')
		print("Working on store: " + store_url)

		all_freq = {}
		for i in store_url: 
			if i in all_freq: 
				all_freq[i] += 1
			else: 
				all_freq[i] = 1

		if (all_freq.get("/") > 2):
			address = soup.findAll(class_="c-address-street-1")[0].text
			city = soup.findAll(class_="c-address-city")[0].text
			state = soup.findAll(class_="c-address-state")[0].text
			zip_code = soup.findAll(class_="c-address-postal-code")[0].text
			phone_number = soup.findAll(class_="Phone-display Phone-display--withLink")[0].text
			df = df.append({'address':address, 'city':city, 'state':state, 'zip_code':zip_code, 'phone_number':phone_number}, ignore_index = True)
		else:
			store_urls2 = soup.findAll("a", class_= "Teaser-titleLink")
			
			for store2 in store_urls2:
				store_url_2 = store2['href']
				page = requests.get(base_url+store_url_2)
				soup = BeautifulSoup(page.content, 'html.parser')
				print("Working on store2: " + store_url_2)

				address = soup.findAll(class_="c-address-street-1")[0].text
				city = soup.findAll(class_="c-address-city")[0].text
				state = soup.findAll(class_="c-address-state")[0].text
				zip_code = soup.findAll(class_="c-address-postal-code")[0].text
				phone_number = soup.findAll(class_="Phone-display Phone-display--withLink")[0].text
		
				df = df.append({'address':address, 'city':city, 'state':state, 'zip_code':zip_code, 'phone_number':phone_number}, ignore_index = True)

df = df.drop_duplicates()
df.to_csv('jewel_osco.csv', index=False, header=True)