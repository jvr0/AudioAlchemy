# AudioAlchemy
![portada](https://github.com/jvr0/AudioAlchemy/blob/main/img/portada.png)


![profile](https://github.com/jvr0/AudioAlchemy/blob/main/img/profile.jpg) El siguiente proyecto consiste en un encargo realizado por la compañía de venta online [El Ártico Discos](https://www.discogs.com/es/seller/elarticodiscos/profile "El Ártico Discos"). Se ha propuesto un trabajo de ingeniería para la actualización automática del inventario. El objetivo es mejorar la ubicación de los items dentro de la plataforma [Discogs](https://www.discogs.com/es/ "Discogs").

**Índice**
1. [Funcionalidad en la API](#funcionalidad)
2. [Creación del entorno gráfico](#grafico)
3. [Creación del pipeline](#pipeline)
4. [Producción en AWS](#aws)

#### 1. Funcionalidad en la API <a name="funcionalidad"></a>

<details>
<summary>Función autentificación</summary>
<br>

```python
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
```
</details>

<details>
<summary>Función lanzamiento</summary>
<br>

```python
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
```
</details>

#### 2. Creación de entorno gráfico <a name="grafico"></a>

- entorno gráfico en streamlit para entregar a cliente
- decoración y colores
- temporizador para activr en x horas
- botón de cancelar
- botón para crear nuevo inventario
- función para actualizar nuevo inventario automáticamente
- creación de un ejecutable

#### 3. Creación del pipeline <a name="pipeline"></a>

- establecer pipeline que permita conectar el entorno gráfico de streamlit con el src hospedado en el ordenador personal

#### 4. Producción en AWS <a name="aws"></a>

- enviar el src a AWS y conectarlo con el streamlit. todo de forma remota en la nube. De esta forma se establece un programa siempre activo que permité la continua iteración de los elementos del inventario en pequeños paquetes (cuentagotas)