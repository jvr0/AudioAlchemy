import os
import io
import sys
import zipfile
import pandas as pd
import requests as req
from requests_oauthlib import OAuth1 

sys.path.append('..')

from config import *

oauth = OAuth1(
        key,
        client_secret=secret,
        resource_owner_key=access_oauth_token,
        resource_owner_secret=access_oauth_token_secret,
        verifier=oauth_verifier)



def autentificacion():
    try:   
        url = f'https://api.discogs.com/oauth/identity'
        res = req.get(url, auth=oauth)
        print('Success')
        print(res.json())
    except:
        print('something is wrong')
        print(res.status_code)



def descarga_inventario(): # función que llama a la API, obtiene una url, descarga el contenido y lo transforma en un csv

    # Obtención del url del último inventario
    url = 'https://api.discogs.com/inventory/export'

    res = req.get(url, auth=oauth)

    url_inv= res.json()['items'][0]['download_url']

    # descarga del ZIP
    res = req.get(url_inv, auth=oauth)

    # escritura
    if res.status_code == 200:
        zip_file = zipfile.ZipFile(io.BytesIO(res.content))

        # guardamos nombre del archivo dentro del ZIP
        csv_file = zip_file.namelist()[0]

        csv_data = zip_file.read(csv_file).decode('utf-8')

        # guardamos el archivo csv
        with open('../data/inventario.csv', 'w', encoding='utf-8') as f:
            f.write(csv_data)
        print("CSV updated as: 'inventario.csv'")
    else:
        print('Something is wrong', res.status_code)



def modificacion(): # función para crear csv de subida

    df = pd.read_csv('../data/inventario.csv') # importamos csv

    df = df[df.status == 'For Sale'] # solo items a la venta

    upload = df.sample(n=2) # se seleccionan dos items aleatorios del inventario

    upload = upload[['listing_id','release_id', 'price']] # dejamos solo las columnas que interesan
    
    upload.price = upload.price - 0.01 # realizamos una pequeña modificación

    upload.price.round(2)

    upload.to_csv('../data/upload.csv', sep=',', index=False) # exportamos

    if os.path.exists('../data/upload.csv'):
        print("File was successfully saved")
        print(upload[['listing_id','release_id', 'price']])
    else:
        print('something went wrong saving the file')



def lanzamiento ():

        url = 'https://api.discogs.com/inventory/upload/change' # url para actualización

        csv_file_path = '../data/upload.csv' # camino hacía los datos

        files = {'upload': ('upload.csv', open(csv_file_path, 'rb'), 'text/csv')} # apertura para lanzamiento

        res = req.post(url, auth=oauth, files=files) # envió a la API

        if res.status_code == 200:
            print('Successful update', res.status_code)
            print(res.headers['X-Discogs-Ratelimit-Remaining'])
    
        else:
            print('Something is wrong', res.status_code)