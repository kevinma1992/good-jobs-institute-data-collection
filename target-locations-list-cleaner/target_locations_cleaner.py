import pandas as pd

store_id = 1

target_locations = pd.read_csv('target_locations.csv')

df = pd.DataFrame(columns = ['store_id','address','state','zip_code'])


for name in target_locations['name']:
	print("working on Store: %s"%name)
	name_array = name.split()
	del name_array[0:4]
	address_array = name_array[0:len(name_array)-3]
	address = ' '.join(address_array).lower().title()
	state = name_array[-3]
	zip_code = name_array[-2]
	df = df.append({'store_id':store_id, 'address':address,'state':state,'zip_code':zip_code}, ignore_index = True)
	store_id = store_id + 1

df.to_csv('target_cleaned.csv', index=False, header=True)


