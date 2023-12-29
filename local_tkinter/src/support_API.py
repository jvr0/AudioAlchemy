import requests as req
import pandas as pd
import zipfile
import io

from src.config import *


def nuevo_inventario():
    url = 'https://api.discogs.com/inventory/export'
    res = req.post(url, auth=oauth)

    if res.status_code == 200 :
        return f'Nuevo inventario creado'
    
    else:
        return f'Something went wrong'

def descarga_inventario(): 

    # Obtención del url del último inventario
    url = 'https://api.discogs.com/inventory/export'

    res = req.get(url, auth=oauth)

    try:
        new_url = res.json()['pagination']['urls']['last']
        res = req.get(new_url, auth=oauth)

        url_inv= res.json()['items'][-1]['download_url']
        fecha = res.json()['items'][-1]['created_ts']
    
    except:
        url_inv= res.json()['items'][-1]['download_url']
        fecha = res.json()['items'][-1]['created_ts']

    # descarga del ZIP
    res = req.get(url_inv, auth=oauth)

    # escritura del archivo
    if res.status_code == 200:
        zip_file = zipfile.ZipFile(io.BytesIO(res.content))

        # guardamos nombre del archivo dentro del ZIP
        csv_file = zip_file.namelist()[0]

        csv_data = zip_file.read(csv_file).decode('utf-8')

        # guardamos el archivo csv
        with open('utopia/data/inventario.csv', 'w', encoding='utf-8') as f:
            f.write(csv_data)
        print(f"CSV updated as: 'inventario.csv' created on: {fecha}")
    else:
        print('Something is wrong', res.status_code)