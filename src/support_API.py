import os
import io
import sys
import time
import zipfile
import pandas as pd
import requests as req
from requests_oauthlib import OAuth1 
import random

import streamlit as st


# Juramento para autentificarse en la API. OAuth1: identificación usuario y contraseña
oauth = OAuth1(
        st.secrets["key"],
        client_secret=st.secrets['secret'],
        resource_owner_key=st.secrets['access_oauth_token'],
        resource_owner_secret=st.secrets['access_oauth_token_secret'],
        verifier=st.secrets['oauth_verifier'])

'''
Función para la devolución del credencial. Utilizada durante el proceso de testo de la API para verificar el status code.
Devuelve el nombre de usuario del vendedor auth(juramento) se este utilizando.
'''
def autentificacion():
    try:   
        url = f'https://api.discogs.com/oauth/identity' # llamada al endpoint
        res = req.get(url, auth=oauth)
        if res.status_code==200:
            return f"Success, welcome: {res.json()['username']}" # devolución del usuario siempre que res=200
        else:
            return f"Something is wrong {res.status_code}"
    except:
        return f"Something is really wrong"

'''
Función para la creación de un nuevo inventario en la plataforma Discogs.
En vez de tener la descarga siempre activa Discogs da la opción de pedir un csv con los datos del inventario para su posterior descarga.
Esta función realiza una llamada post al endpoint y crea un nuevo csv que posteriormente se descargará.
'''
def nuevo_inventario():
    url = 'https://api.discogs.com/inventory/export'
    res = req.post(url, auth=oauth)
    # Poneer un timer

    if res.status_code == 200 :
        return f'New inventory succesfully created'
    
    else:
        return f'Something went wrong'
    

'''
Función que llama a la API y obtiene la URL del último inventario pedido a Discogs, el cual se da en el res en formato ZIP.
También abre el ZIP y lo descarga en la ruta especificada.
'''
def descarga_inventario(): # función que llama a la API, obtiene una url, descarga el contenido y lo transforma en un csv

    # Obtención del url del último inventario
    url = 'https://api.discogs.com/inventory/export'

    res = req.get(url, auth=oauth)

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
        with open('data/inventario.csv', 'w', encoding='utf-8') as f:
            f.write(csv_data)
        print(f"CSV updated as: 'inventario.csv' created on: {fecha}")
    else:
        print('Something is wrong', res.status_code)


'''
Función específica para el entorno gráfico de streamlit.
Realiza lo mismo que la función descarga_inventario, pero en vez de guardarlo en la ruta descarga el inventario en el navegador del usuario.
'''
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


'''
Función que modifica el número de items especificados en el inventario (argumento paquete = nºitems aleatorios a modificar).
Lo primero guarda solo los items a la venta, para no entrar en conflicto con el resto del inventario.
A continuación, aumenta en .01 el precio del item para su actualización.
Devuelve un csv con las columnas listing_id, release_id (requeridas por la API) y price.
Guarda el csv en la ruta especificada para su posterior envio a la API.
'''
def modificacion_precio_aumento(paquete): # función para crear csv de subida

    df = pd.read_csv('data/inventario.csv') # importamos csv

    upload = df[df.status == 'For Sale'] # solo items a la venta

    upload = upload.sample(n=paquete) # se seleccionan dos items aleatorios del inventario

    upload = upload[['listing_id','release_id', 'price']] # dejamos solo las columnas que interesan
    
    upload.price = upload.price + 0.01 # realizamos una pequeña modificación

    upload.price.round(2)

    upload.to_csv('data/upload.csv', sep=',', index=False) # exportamos

    if os.path.exists('data/upload.csv'):
        return ("File was successfully saved", "\n" ,upload[['listing_id','release_id', 'price']])
    else:
        return ('something went wrong saving the file')

'''
Función para aumentar el precio. Usa la función modificación_precio_aumento para preparar el csv a enviar.
Según requisito de la API abre el csv con el modo 'rb' read-binary.
realiza la llamada post al endpoint correspondiente y devuelve una frase según la respuesta de la API.
'''
def lanzamiento_precio_aumento (paquete):
    modificacion_precio_aumento(paquete)

    url = 'https://api.discogs.com/inventory/upload/change' # url para actualización

    csv_file_path = 'data/upload.csv' # camino hacía los datos

    files = {'upload': ('upload.csv', open(csv_file_path, 'rb'), 'text/csv')} # apertura para lanzamiento

    res = req.post(url, auth=oauth, files=files) # envió a la API

    if res.status_code == 200:
        return ('!!Actualización exitosa¡¡ Tienes otras ', res.headers['X-Discogs-Ratelimit-Remaining'], 'llamadas.')
    else:
        return ('Something is wrong', res.status_code)
    

'''
Función que modifica el número de items especificados en el inventario (argumento paquete = nºitems aleatorios a modificar).
Lo primero guarda solo los items a la venta, para no entrar en conflicto con el resto del inventario.
A continuación, resta en .01 el precio del item para su actualización.
Devuelve un csv con las columnas listing_id, release_id (requeridas por la API) y price.
Guarda el csv en la ruta especificada para su posterior envio a la API.
'''
def modificacion_precio_resta(paquete): # función para crear csv de subida

    df = pd.read_csv('data/inventario.csv') # importamos csv

    upload = df[df.status == 'For Sale'] # solo items a la venta

    upload = upload.sample(n=paquete) # se seleccionan dos items aleatorios del inventario

    upload = upload[['listing_id','release_id', 'price']] # dejamos solo las columnas que interesan
    
    upload.price = upload.price - 0.01 # realizamos una pequeña modificación

    upload.price.round(2)

    upload.to_csv('data/upload.csv', sep=',', index=False) # exportamos

    if os.path.exists('data/upload.csv'):
        return ("File was successfully saved", "\n" ,upload[['listing_id','release_id', 'price']])
    else:
        return ('something went wrong saving the file')


'''
Función para aumentar el precio. Usa la función modificación_precio_resta para preparar el csv a enviar.
Según requisito de la API abre el csv con el modo 'rb' read-binary.
realiza la llamada post al endpoint correspondiente y devuelve una frase según la respuesta de la API.
'''
def lanzamiento_precio_resta (paquete):
    modificacion_precio_resta(paquete)

    url = 'https://api.discogs.com/inventory/upload/change' # url para actualización

    csv_file_path = 'data/upload.csv' # camino hacía los datos

    files = {'upload': ('upload.csv', open(csv_file_path, 'rb'), 'text/csv')} # apertura para lanzamiento

    res = req.post(url, auth=oauth, files=files) # envió a la API

    if res.status_code == 200:
        return ('!!Actualización exitosa¡¡ Tienes otras ', res.headers['X-Discogs-Ratelimit-Remaining'], 'llamadas.')
    else:
        return ('Something is wrong', res.status_code)


'''
Función específica del entorno gráfico streamlit.
Esta función utiliza las explicadas anteriormente para realizar un proceso completo de envió de datos a la API.
En primer lugar realiza una request post a la API para solicitar un nuevo inventario.
Espera 10 segundos (para dar tiempo a Discogs de procesar) y a continuación descarga el nuevo inventario almacenandolo en la ruta especificada.
A continuación realiza una selección aleatoria de 50/50 para elegir que tipo de lanzamiento procesar, la suma o la resta.

Esta función se utilizará principalmente para las actualizaciones que usen temporizador en streamlit. Debido a que la idea del cliente es mantener
en funcionamiento continuo el temporizador el sistema de selección random tendrá un efecto mínimo en el precio de los productos. Las dos opciones
tienen los mismos pesos por lo que no habrá una diferencia significativa. Se ha creado esta función con la idea de que cada x tiempo, seleccionado
por el cliente, se ejecute.
'''

def programado_suma():

    df = pd.read_csv('data/inventario.csv') # importamos csv

    upload = df[df.status == 'For Sale'] # solo items a la venta

    upload = upload[['listing_id','release_id', 'price']] # dejamos solo las columnas que interesan
    
    upload.price = upload.price + 0.01 # realizamos una pequeña modificación

    upload.price.round(2)

    upload.to_csv('data/upload.csv', sep=',', index=False) # exportamos

    url = 'https://api.discogs.com/inventory/upload/change' # url para actualización

    csv_file_path = 'data/upload.csv' # camino hacía los datos

    files = {'upload': ('upload.csv', open(csv_file_path, 'rb'), 'text/csv')} # apertura para lanzamiento

    res = req.post(url, auth=oauth, files=files) # envió a la API

    if res.status_code == 200:
        return ('!!Actualización exitosa¡¡ Tienes otras ', res.headers['X-Discogs-Ratelimit-Remaining'], 'llamadas.')
    else:
        return ('Something is wrong', res.status_code)
    
def programado_resta():

    df = pd.read_csv('data/inventario.csv') # importamos csv

    upload = df[df.status == 'For Sale'] # solo items a la venta

    upload = upload[['listing_id','release_id', 'price']] # dejamos solo las columnas que interesan
    
    upload.price = upload.price - 0.01 # realizamos una pequeña modificación

    upload.price.round(2)

    upload.to_csv('data/upload.csv', sep=',', index=False) # exportamos

    url = 'https://api.discogs.com/inventory/upload/change' # url para actualización

    csv_file_path = 'data/upload.csv' # camino hacía los datos

    files = {'upload': ('upload.csv', open(csv_file_path, 'rb'), 'text/csv')} # apertura para lanzamiento

    res = req.post(url, auth=oauth, files=files) # envió a la API

    if res.status_code == 200:
        return ('!!Actualización exitosa¡¡ Tienes otras ', res.headers['X-Discogs-Ratelimit-Remaining'], 'llamadas.')
    else:
        return ('Something is wrong', res.status_code)


def lanzamiento_programado():

    nuevo_inventario() # llamada para pedir un nuevo inventario

    time.sleep(10)

    descarga_inventario() # llamada para descargar el nuevo inventario

    time.sleep(5)

    elegir = random.randint(1,2) # selección aleatoria del tipo de lanzamiento
    if elegir == 1:
        programado_suma() # lanzamiento de resta .01
    else:
        programado_resta() # lanzamiento de suma .01

    print(elegir) # índica que tipo de lanzamiento se ha llevado a cabo
    
    return '¡Actualización correctamente programada!'

'''
Las siguientes dos funciones estan destinadas a ser utilizadas dentro del despliegue en streamlit.
Reciven una categoría, en este caso un sello discográfico introducido por el usuario.
Se realiza la filtración del df a través de dicha categoría y se resta el precio de los items en .01
Finalmente se envia el archivo resultante al endpoint para la actualización de los items.
'''
def modificacion_categoria(categoria): 
    df = pd.read_csv('data/inventario.csv') 

    # Filtrar por la categoría seleccionada en las columnas 'label' y 'artist'
    filtro = (df['label'] == categoria)
    upload = df[filtro & (df['status'] == 'For Sale')]

    # Realizar la modificación en el precio
    if not upload.empty:
        upload['price'] = upload['price'] - 0.01
        upload['price'] = upload['price'].round(2)

        # Guardar el DataFrame modificado en un nuevo CSV
        upload[['listing_id', 'release_id', 'price']].to_csv('data/upload.csv', sep=',', index=False)

        if os.path.exists('data/upload.csv'):
            return "El archivo se guardó exitosamente. Datos modificados:\n", upload[['listing_id', 'release_id', 'price']]
        else:
            return 'Hubo un problema al guardar el archivo.'
    else:
        return 'No se encontraron elementos para la categoría seleccionada.'
    
def lanzamiento_precio_resta_categoria (categoria):
    modificacion_categoria(categoria)

    url = 'https://api.discogs.com/inventory/upload/change' # url para actualización

    csv_file_path = 'data/upload.csv' # camino hacía los datos

    files = {'upload': ('upload.csv', open(csv_file_path, 'rb'), 'text/csv')} # apertura para lanzamiento

    res = req.post(url, auth=oauth, files=files) # envió a la API

    if res.status_code == 200:
        return ('!!Actualización exitosa¡¡ Tienes otras ', res.headers['X-Discogs-Ratelimit-Remaining'], 'llamadas.')
    else:
        return ('Something is wrong', res.status_code)
    

'''
Las siguientes dos funciones estan destinadas a ser utilizadas dentro del despliegue en streamlit.
Reciven un artista introducido por el usuario.
Se realiza la filtración del df a través de dicho artista y se resta el precio de los items en .01
Finalmente se envia el archivo resultante al endpoint para la actualización de los items.
'''
def modificacion_artista(artista): 
    df = pd.read_csv('data/inventario.csv') 

    # Filtrar por la categoría seleccionada en las columnas 'label' y 'artist'
    filtro = (df['artist'] == artista)
    upload = df[filtro & (df['artista'] == 'For Sale')]

    # Realizar la modificación en el precio
    if not upload.empty:
        upload['price'] = upload['price'] - 0.01
        upload['price'] = upload['price'].round(2)

        # Guardar el DataFrame modificado en un nuevo CSV
        upload[['listing_id', 'release_id', 'price']].to_csv('data/upload.csv', sep=',', index=False)

        if os.path.exists('data/upload.csv'):
            return "El archivo se guardó exitosamente. Datos modificados:\n", upload[['listing_id', 'release_id', 'price']]
        else:
            return 'Hubo un problema al guardar el archivo.'
    else:
        return 'No se encontraron elementos para la categoría seleccionada.'
    
def lanzamiento_precio_resta_artista (artista):
    modificacion_artista(artista)

    url = 'https://api.discogs.com/inventory/upload/change' # url para actualización

    csv_file_path = 'data/upload.csv' # camino hacía los datos

    files = {'upload': ('upload.csv', open(csv_file_path, 'rb'), 'text/csv')} # apertura para lanzamiento

    res = req.post(url, auth=oauth, files=files) # envió a la API

    if res.status_code == 200:
        return ('!!Actualización exitosa¡¡ Tienes otras ', res.headers['X-Discogs-Ratelimit-Remaining'], 'llamadas.')
    else:
        return ('Something is wrong', res.status_code)