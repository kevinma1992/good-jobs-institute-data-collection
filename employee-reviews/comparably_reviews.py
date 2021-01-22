import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

df = pd.DataFrame(columns = ['store_name','dimension_name','score'])

urls = ["https://www.comparably.com/companies/food-4-less/culture", 
"https://www.comparably.com/companies/wegmans/culture",
"https://www.comparably.com/companies/trader-joes/culture",
"https://www.comparably.com/companies/costco/culture",
"https://www.comparably.com/companies/aldi-usa/culture",
"https://www.comparably.com/companies/natural-grocers-by-vitamin-cottage/culture",
"https://www.comparably.com/companies/the-fresh-market/culture",
"https://www.comparably.com/companies/publix-super-markets/culture",
"https://www.comparably.com/companies/winco-foods/culture",
"https://www.comparably.com/companies/grocery-outlet/culture",
"https://www.comparably.com/companies/sprouts-farmers-market/culture",
"https://www.comparably.com/companies/stater-bros-91734/culture",
"https://www.comparably.com/companies/harris-teeter/culture",
"https://www.comparably.com/companies/whole-foods-market/culture",
"https://www.comparably.com/companies/ingles-markets/culture",
"https://www.comparably.com/companies/food-lion/culture",
"https://www.comparably.com/companies/hannaford-bro/culture",
"https://www.comparably.com/companies/sam-s-club/culture",
"https://www.comparably.com/companies/ralphs/culture",
"https://www.comparably.com/companies/giant-food/culture",
"https://www.comparably.com/companies/smith-s-food-and-drug/culture",
"https://www.comparably.com/companies/giant-food-stores-llc/culture",
"https://www.comparably.com/companies/363484/culture",
"https://www.comparably.com/companies/shoprite-supermarkets/culture",
"https://www.comparably.com/companies/target/culture",
"https://www.comparably.com/companies/vons/culture",
"https://www.comparably.com/companies/meijer/culture",
"https://www.comparably.com/companies/fred-meyer/culture",
"https://www.comparably.com/companies/kroger/culture",
"https://www.comparably.com/companies/winn-dixie-stores/culture",
"https://www.comparably.com/companies/jewel-osco/culture",
"https://www.comparably.com/companies/save-a-lot/culture",
"https://www.comparably.com/companies/giant-eagle/culture",
"https://www.comparably.com/companies/king-soopers/culture",
"https://www.comparably.com/companies/stop-shop/culture",
"https://www.comparably.com/companies/safeway/culture",
"https://www.comparably.com/companies/acme-markets/culture",
"https://www.comparably.com/companies/walmart/culture",
"https://www.comparably.com/companies/h-e-b/culture"
]

for url in urls:
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	store_name = soup.findAll(itemprop="name")[0].text
	print("Working on store: " + store_name)
	overall_score = soup.findAll(class_="numberGrade-score")[0].text
	dictionary = {
		"store_name": store_name,
		"dimension_name": "overall_score",
		"score": overall_score
	}
	df = df.append(dictionary, ignore_index = True)

	culture_dimensions = soup.findAll(class_="gs-col gs-col-1-2")

	for dimension in culture_dimensions:
		dimension_name = dimension.findAll(class_="section-subtitle")[0].text
		try:
			score = dimension.findAll(class_="numberGrade-score")[0].text
		except:
			score = np.nan
			print("No Score for Dimension: %s"%dimension_name)
		df = df.append({'store_name':store_name, 'dimension_name':dimension_name, 'score':score}, ignore_index = True)

df.to_csv('comparably_reviews_test.csv', index=False, header=True)


