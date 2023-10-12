from fileinput import filename
import requests
import pandas as pd
from datetime import datetime
import time

URL = 'https://tienda.mercadona.es/api/v1_1/categories/'


categories_r = requests.get(URL).json()['results']


categories = {}
for cat in categories_r:
    categories[cat['name']] = requests.get(URL + str(cat['id'])).json()['categories']
    time.sleep(0.1)


products = pd.DataFrame()
for cat, js in categories.items():
    for subcat in js:
        cat_products = pd.json_normalize(subcat['products'])
        cat_products['category'] = cat
        cat_products['subcategory'] = subcat['name']

        products = pd.concat([products, cat_products])
products


filename = 'data/' + datetime.now().strftime('%d-%m-%y') + '.csv'
products.to_csv(filename)