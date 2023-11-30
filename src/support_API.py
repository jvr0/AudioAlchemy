import os
import io
import sys
import time
import zipfile
import pandas as pd
import requests as req
from requests_oauthlib import OAuth1 
import random

sys.path.append('..')

from config import *
from support_st import *

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
        if res.status_code==200:
            return f"Success, welcome: {res.json()['username']}"
        else:
            return f"Something is wrong {res.status_code}"
    except:
        return f"Something is really wrong"



def nuevo_inventario(): # función que llama a la API y le pide la creación de un nuevo inventario. Tb actualiza streamlit
    url = 'https://api.discogs.com/inventory/export'
    res = req.post(url, auth=oauth)

    if res.status_code == 200 :
        tamaño_inventario() # actualización streamlit
        return f'New inventory succesfully created'
    
    else:
        return f'Something went wrong'
    


def descarga_inventario(): # función que llama a la API, obtiene una url, descarga el contenido y lo transforma en un csv

    # Obtención del url del último inventario
    url = 'https://api.discogs.com/inventory/export'

    res = req.get(url, auth=oauth)

    url_inv= res.json()['items'][-1]['download_url']
    fecha = res.json()['items'][-1]['created_ts']

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
        print(f"CSV updated as: 'inventario.csv' created on: {fecha}")
    else:
        print('Something is wrong', res.status_code)



def descarga_streamlit(): # función que llama a la API, obtiene una url, descarga el contenido en streamlit

    # Obtención del url del último inventario
    url = 'https://api.discogs.com/inventory/export'

    res = req.get(url, auth=oauth)

    url_inv= res.json()['items'][0]['download_url']

    # descarga del ZIP
    res = req.get(url_inv, auth=oauth)

    # escritura
    if res.status_code == 200:
        zip_file = zipfile.ZipFile(io.BytesIO(res.content))

        # Guardamos el nombre del archivo CSV dentro del ZIP
        csv_file = zip_file.namelist()[0]

        # Extraemos el contenido del archivo CSV
        content = zip_file.read(csv_file).decode('utf-8')

        return content
    else:
        return None



def modificacion_precio_aumento(paquete): # función para crear csv de subida

    df = pd.read_csv('../data/inventario.csv') # importamos csv

    upload = df[df.status == 'For Sale'] # solo items a la venta

    upload = upload.sample(n=paquete) # se seleccionan dos items aleatorios del inventario

    upload = upload[['listing_id','release_id', 'price']] # dejamos solo las columnas que interesan
    
    upload.price = upload.price + 0.01 # realizamos una pequeña modificación

    upload.price.round(2)

    upload.to_csv('../data/upload.csv', sep=',', index=False) # exportamos

    if os.path.exists('../data/upload.csv'):
        return ("File was successfully saved", "\n" ,upload[['listing_id','release_id', 'price']])
    else:
        return ('something went wrong saving the file')


def lanzamiento_precio_aumento (paquete):
    modificacion_precio_aumento(paquete)

    url = 'https://api.discogs.com/inventory/upload/change' # url para actualización

    csv_file_path = '../data/upload.csv' # camino hacía los datos

    files = {'upload': ('upload.csv', open(csv_file_path, 'rb'), 'text/csv')} # apertura para lanzamiento

    res = req.post(url, auth=oauth, files=files) # envió a la API

    if res.status_code == 200:
        return ('!!Actualización exitosa¡¡ Tienes otras ', res.headers['X-Discogs-Ratelimit-Remaining'], 'llamadas.')
    else:
        return ('Something is wrong', res.status_code)
    

def modificacion_precio_resta(paquete): # función para crear csv de subida

    df = pd.read_csv('../data/inventario.csv') # importamos csv

    upload = df[df.status == 'For Sale'] # solo items a la venta

    upload = upload.sample(n=paquete) # se seleccionan dos items aleatorios del inventario

    upload = upload[['listing_id','release_id', 'price']] # dejamos solo las columnas que interesan
    
    upload.price = upload.price - 0.01 # realizamos una pequeña modificación

    upload.price.round(2)

    upload.to_csv('../data/upload.csv', sep=',', index=False) # exportamos

    if os.path.exists('../data/upload.csv'):
        return ("File was successfully saved", "\n" ,upload[['listing_id','release_id', 'price']])
    else:
        return ('something went wrong saving the file')


def lanzamiento_precio_resta (paquete):
    modificacion_precio_resta(paquete)

    url = 'https://api.discogs.com/inventory/upload/change' # url para actualización

    csv_file_path = '../data/upload.csv' # camino hacía los datos

    files = {'upload': ('upload.csv', open(csv_file_path, 'rb'), 'text/csv')} # apertura para lanzamiento

    res = req.post(url, auth=oauth, files=files) # envió a la API

    if res.status_code == 200:
        return ('!!Actualización exitosa¡¡ Tienes otras ', res.headers['X-Discogs-Ratelimit-Remaining'], 'llamadas.')
    else:
        return ('Something is wrong', res.status_code)

def lanzamiento_programado(paquete):

    nuevo_inventario()

    time.sleep(10)

    descarga_inventario()

    time.sleep(5)

    elegir = random.randint(1,2)
    if elegir == 1:
        lanzamiento_precio_resta(paquete)
    else:
        lanzamiento_precio_aumento(paquete)

    print(elegir)
    
    return '¡Actualización correctamente programada!'


def comentario(x):
    if x is not np.nan: 
        x = str(x)
        x = x + "⚡️"
        return x

def modificacion_comentario(paquete): # función para crear csv de subida

    df = pd.read_csv('../data/inventario.csv') # importamos csv

    upload = df[df.status == 'For Sale'] # solo items a la venta

    upload = upload.sample(n=paquete) # se seleccionan dos items aleatorios del inventario

    upload = upload[['listing_id','release_id', 'comments']] # dejamos solo las columnas que interesan
    
    upload.comments = upload.comments.apply(comentario) # realizamos una pequeña modificación

    upload.to_csv('../data/upload.csv', sep=',', index=False) # exportamos

    if os.path.exists('../data/upload.csv'):
        return ("File was successfully saved", "\n" ,upload[['listing_id','release_id', 'comments']])
    else:
        return ('something went wrong saving the file')

def lanzamiento_comentario (paquete):
    modificacion_comentario(paquete)

    url = 'https://api.discogs.com/inventory/upload/change' # url para actualización

    csv_file_path = '../data/upload.csv' # camino hacía los datos

    files = {'upload': ('upload.csv', open(csv_file_path, 'rb'), 'text/csv')} # apertura para lanzamiento

    res = req.post(url, auth=oauth, files=files) # envió a la API

    if res.status_code == 200:
        return ('!!Actualización exitosa¡¡ Tienes otras ', res.headers['X-Discogs-Ratelimit-Remaining'], 'llamadas.')

    else:
        return ('Something is wrong', res.status_code)