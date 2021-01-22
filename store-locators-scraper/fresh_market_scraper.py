import requests
from bs4 import BeautifulSoup
import pandas as pd

store_id = 1

df = pd.DataFrame(columns = ['store_id','address','address2'])

url = "https://www.thefreshmarket.com/your-market/store-locator"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
addresses = soup.findAll(class_="store-list-item-address__row")

for index in range(int(len(addresses)/2)):
	address = addresses[index*2].text
	address2 = addresses[index*2+1].text
	df = df.append({'store_id':store_id, 'address':address, 'address2':address2}, ignore_index = True)
	store_id = store_id + 1

df.to_csv('fresh_market.csv', index=False, header=True)


