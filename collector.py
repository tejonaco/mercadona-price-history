import requests, time, json


URL = 'https://tienda.mercadona.es/api/categories/'

# funcion recursiva que escaneara la api

def fillProducts(url: str, content: list, products: list = [], root = 'categories', repeatIfDenied: int = 3):
	'''url: enlace donde se encuentra el siguiente json a analizar
	content: lista referenciada fuera de la funcion a rellenar con los datos de ese json
	products: lista de productos vista en el anterior json, si no se encuentran mas json seran los productos definitivos
	root: raiz del json donde buscar una lista de categorias
	repeatIfDenied: si el servidor se quejara de que se estan lanzando demasiadas llamadas se reintenta este numero de veces
	'''
    
	r = requests.get(url)
	if r.status_code == 200: # estamos viendo CATEGORIA GENERAL, CATEGORIA ESPECIFICA o TIPO DE PRODUCTO
		for item in r.json()[root]:
			content.append(
				{
					'id': item['id'],
					'name': item['name'],
					'content': [],
					}
					)
			time.sleep(2) # retraso para no sobrecargar el servidor
			fillProducts(
				url = URL + str(item['id']),
				content = content[-1]['content'],
				products = item.get('products', []),
				)
	elif r.status_code == 429: # Solicitud denegada por recibir demasiadas peticiones seguidas
			time.sleep(60)
			# se vuelve a intentar una vez mas
			if repeatIfDenied:
				fillProducts(
						url = url,
						content = content,
						products = products,
						repeatIfDenied = repeatIfDenied - 1
						)
			else:
				raise Exception('Solicitud denegada por recibir demasiadas peticiones seguidas')
								
	elif r.status_code == 410: # ya no hay mas sublistas
		for item in products:
			pi = item['price_instructions']

			product = {
				'id': item['id'],
				'name': item['display_name'],
				'iva': pi['iva'],
				'unit_size': pi['unit_size'],
				'bulk_price': pi['bulk_price'],
				'unit_price': pi['unit_price'],
				'size_format': pi['size_format'],
				}
			
			content.append(product)
			time.sleep(1) # retraso para no sobrecargar el servidor


# rellenar los datos
products = []
fillProducts(url=URL, content=products, root='results')

# grabarlos en un json, que se irá guardando en la historia de git
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(products, f,
              indent='\t' # + legible
              , ensure_ascii=False # para que aparezcan las tildes
			  )