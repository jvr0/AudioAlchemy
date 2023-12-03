![portada](https://github.com/jvr0/AudioAlchemy/blob/main/img/portada.png)

El siguiente proyecto consiste en un encargo realizado por la compañía de venta online [El Ártico Discos](https://www.discogs.com/es/seller/elarticodiscos/profile "El Ártico Discos"). Se ha propuesto un trabajo de ingeniería para la actualización automática del inventario. El objetivo es mejorar la ubicación de los items dentro de la plataforma [Discogs](https://www.discogs.com/es/ "Discogs").

**Índice**
1. [API](#API)
2. [Puesta en producción](#produccion)
    2.1[AWS](#AWS)
    2.2 [Streamlit](#streamlit)

#### 1. API <a name="API"></a>

##### Validación app

El primer paso para la utilización de la api es la creación de una app en la: [web developer Discogs](https://www.discogs.com/es/settings/developers "web developer Discogs"). A continuación será necesario validar esta APP. Para mayor información de cómo validar la app ver el notebook [authorization](https://github.com/jvr0/AudioAlchemy/blob/main/notebooks/authorization.ipynb "authorization.ipynb"). Si fuera necesaria más documentación sobre esta API se puede encontrar en el siguiente [enlace](https://www.discogs.com/developers/# "enlace"). A continuación la estructura de la variable auth:

<details>
<summary>Estructura de Auth</summary>
<br>

```python
oauth = OAuth1(
        key],
        client_secret=secret],
        resource_owner_key=access_oauth_token,
        resource_owner_secret=access_oauth_token_secret,
        verifier=oauth_verifier
        )
```
</details>

##### Endpoints
Los endpoints utilizados para este proyecto son aquellos relacionados con el manejo y actualización del inventario. A continuación los ejemplos de uso. Para más información sobre el uso de los endpoints: [SRC](https://github.com/jvr0/AudioAlchemy/blob/main/src/support_API.py "SRC")

<details>
<summary>descarga_inventario</summary>
<br>

```python
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
```
</details>

<details>
<summary>descarga_streamlit</summary>
<br>

```python
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
```
</details>

<details>
<summary>modificacion_precio_resta</summary>
<br>

```python
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
```
</details>

<details>
<summary>lanzamiento_precio_resta</summary>
<br>

```python
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
```
</details>

<details>
<summary>lanzamiento_programado</summary>
<br>

```python
def lanzamiento_programado(paquete):

    nuevo_inventario() # llamada para pedir un nuevo inventario

    time.sleep(10)

    descarga_inventario() # llamada para descargar el nuevo inventario

    time.sleep(5)

    elegir = random.randint(1,2) # selección aleatoria del tipo de lanzamiento
    if elegir == 1:
        lanzamiento_precio_resta(paquete) # lanzamiento de resta .01
    else:
        lanzamiento_precio_aumento(paquete) # lanzamiento de suma .01

    print(elegir) # índica que tipo de lanzamiento se ha llevado a cabo
    
    return '¡Actualización correctamente programada!'
```
</details>

##### Formato de Archivos
A la hora de la recepción y envío de archivos en la API se debe tener en cuenta lo siguiente:

<details>
<summary>Consideraciones sobre archivos</summary>
<br>

1. El archivo recibido en el endpoint ```url = 'https://api.discogs.com/inventory/export'``` será un ZIP, por lo que es necesaria la librería ```zipfile``` para poder descomprimirlo y abrirlo.
2. El archivo enviado para actualizar archivos al endpoint ```url = 'https://api.discogs.com/inventory/upload/change'``` debe ser un csv que previamente haya sido abierto en nuestro código.
3. El archivo csv enviado requería que se siguierá estrictamente el siguiente formato\n```listing_id,release_id,price``` siendo price la columna que se desea modificar entre las opciones que se pueden encontrar en la documentación de la propia API.
</details>

#### 2. Puesta en producción <a name="produccion"></a>