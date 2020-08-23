from bs4 import BeautifulSoup
import requests
import csv
import json

URL_BASE ="https://www.tottus.cl{}"
URL = URL_BASE.format("/api/product-search/by-category-slug?slug=cervezas-cat010403&sort=score&page=1&perPage=500")
FILECSV = "cervezas-tottus.csv"
TOTAL=0

with open(FILECSV, 'w', newline='') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(['Name', 'Description', 'regularPrice', 'currentPrice', 'Image'])

def beer(url,np=1):
    global TOTAL
    req = requests.get(url)
    statusCode = req.status_code

    if statusCode == 200:
        html = BeautifulSoup(req.text, "html.parser")
        entradas = json.loads(html.text)

        for entrada in entradas['results']:
            name = entrada['name']
            #Images 
            if len(entrada['images'])>0:
                image = entrada['images'][0]
            else:
                image = 'https://www.tottus.cl/static/images/temp/placeholder-image.jpg'
            desc = entrada['description']

            #Prices
            if len(entrada['prices']) > 0:
                regularPrice = entrada['prices']['regularPrice']
                currentPrice = entrada['prices']['currentPrice']
            else:
                regularPrice = ''
                currentPrice = ''

            with open(FILECSV, 'a', newline='') as csvfile:
                datawriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                datawriter.writerow([str(name), str(desc), str(regularPrice), str(currentPrice), str(image)])

            TOTAL+=1
        print(TOTAL)
        # Solo considera leer un JSON, por lo que no es necesario paginación
beer(URL)