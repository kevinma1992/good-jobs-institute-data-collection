import requests
from bs4 import BeautifulSoup
import pandas as pd

df = pd.DataFrame(columns = ['address','city','state','zip_code','phone_number'])

base_url = "https://local.safeway.com/"

company_url = "https://local.safeway.com/safeway.html"
page = requests.get(company_url)
soup = BeautifulSoup(page.content, 'html.parser')
state_urls = soup.findAll("a",class_="Directory-listLink")

for state in state_urls:
	state_url = state['href']
	print('Working on state:'+state_url)
	page = requests.get(base_url+state_url)
	soup = BeautifulSoup(page.content, 'html.parser')

	city_urls = soup.findAll("a", class_= "Directory-listLink")

	for city in city_urls:
		city_url = city['href']

		page = requests.get(base_url+city_url)
		soup = BeautifulSoup(page.content, 'html.parser')
		print("Working on city: " + city_url)

		all_freq = {}
		for i in city_url: 
			if i in all_freq: 
				all_freq[i] += 1
			else: 
				all_freq[i] = 1

		if (all_freq.get("/") > 3):
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
df.to_csv('safeway.csv', index=False, header=True)