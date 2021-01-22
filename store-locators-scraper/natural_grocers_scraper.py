import requests
from bs4 import BeautifulSoup
import pandas as pd

store_id = 1

df = pd.DataFrame(columns = ['store_id','address','city','state','zip_code','phone_number'])

for page_num in range(14):
	url = "https://www.naturalgrocers.com/store-directory?field_store_address_administrative_area=All&page=%d"%page_num
	print("Working on Page %d"%page_num)
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	addresses = soup.findAll(class_="address-line1")
	cities = soup.findAll(class_="locality")
	states = soup.findAll(class_="administrative-area")
	zip_codes = soup.findAll(class_="postal-code")
	phone_numbers = soup.findAll(class_="store_telephone_number")

	for index in range(len(addresses)):
		address = addresses[index].text
		city = cities[index].text
		state = states[index].text
		zip_code = zip_codes[index].text
		phone_number = phone_numbers[index].text.strip()
		df = df.append({'store_id':store_id, 'address':address, 'city':city, 'state':state, 'zip_code':zip_code, 'phone_number':phone_number}, ignore_index = True)
		store_id = store_id + 1

df.to_csv('natural_grocers.csv', index=False, header=True)


