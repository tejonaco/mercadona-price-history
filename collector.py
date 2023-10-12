import requests, time, json
from collections import OrderedDict


URL = 'https://tienda.mercadona.es/api/categories/'


categories = requests.get(URL).json()['results']


data = {}
for cat in categories:
    # guardamos la categoría por su nombre, necesitamos el id para obtener la url
    cat_name = cat['name']
    cat_url = URL + str(cat['id'])

    # dentro de cada categoria estan las subcategorias
    for subcat in requests.get(cat_url).json()['categories']:
        # dentro de la subcategoria los productos
        subcat_name, subcat_products = subcat['name'], subcat['products']
        # de cada producto nos quedaremos con:
        # - id [id] -> se usará como índice, suponiendo que será mas estable que el nombre
        # - nombre [display_name]
        ## price_instructions
            # - iva [iva]
            # - tamaño [unit_size]
            # - precio por kg/L... [bulk_price]
            # - precio por unidad [unit_price]
            # - unidades del formato [size_format]
        for product in subcat_products:
            product_id = product['id']
            pi = product['price_instructions']
            data[product_id] = {
                'name': product['display_name'],
                'iva': pi['iva'],
                'unit_size': pi['unit_size'],
                'bulk_price': pi['bulk_price'],
                'unit_price': pi['unit_price'],
                'size_format': pi['size_format'],
                'category': cat_name,
                'subcategory': subcat_name
            }

    time.sleep(0.5) # esperar un poco entre llamadas a la API



# organizamos los datos por id, por tenerlos siempre de la misma manera
dataSorted = OrderedDict(
    sorted(data.items(), key=lambda k: float(k[0]))
    )


# guardamos el resultado en un json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(dataSorted, f,
              indent='\t' # + legible
              , ensure_ascii=False # para que aparezcan las tildes
              )