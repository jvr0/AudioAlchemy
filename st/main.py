import streamlit as st
import pandas as pd
import schedule
import time
import subprocess
from PIL import Image
import webbrowser
import base64
import io

import sys
sys.path.append('../src')
from support_API import *
from support_st import *


# CONFIG INICIAL
st.set_page_config(
    page_title="AudioAlchemy",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded",)

size = tamaño_inventario()

st.set_option('deprecation.showPyplotGlobalUse', False)


def pagina_inicio():
    # MURO

    # ACTUALIZAR AHORA

    st.write(f'### Actualizar ahora')

    paquete = st.number_input("Ingresa el tamaño del paquete a enviar (min 2)",
                                value=2,
                                min_value=2,
                                max_value=size,
                                step=1)
    st.write(f"El paquete que se enviará es de: {paquete}")

    if st.button (f':green[Actualizar sumando al precio]'):
            user = lanzamiento_precio_aumento(paquete)
            st.info(user)

    if st.button (f':green[Actualizar restando al precio]'):
            user = lanzamiento_precio_resta(paquete)
            st.info(user)

    # PROGRAMAR ACTUALIZACIÓN

    st.write(f'### Programar actualización')

    # Widget para seleccionar la hora
    hora = st.slider("Selecciona la hora", 0, 23, 9)  # Valores de 0 a 23 para las horas

    programacion_activa = False


    def activar_programacion(hora, paquete):
        global programacion_activa
        schedule.every().day.at(f"{hora:02d}:23").do(lanzamiento_programado, paquete).tag(f"{hora}")

    def cancelar_programacion():
        global programacion_activa
        schedule.clear()

    if st.button(":green[Programar]"):
        activar_programacion(hora, paquete)
        programacion_activa = True

    if st.button(":red[Cancelar]"):
        cancelar_programacion()
        programacion_activa = False

    st.write(schedule.get_jobs())

    if programacion_activa == True:
        st.write(f':green[Estado de la programación: {programacion_activa}]')
    else:
        st.write(f':red[Estado de la programación: {programacion_activa}]')

    # Estado de la programación y ejecutar tareas programadas
    while True:
        if programacion_activa == True:
            schedule.run_pending()  # Ejecutar tareas programadas
            time.sleep(2)
        else:
            time.sleep(2)

def statistics():
    df = df = pd.read_csv('../data/inventario.csv')
    df = df[df.status == 'For Sale']

    st.title("Estadísticas")

    size = tamaño_inventario()
    mean = round(df.price.mean(),2)
    st.write(f'#### Tamaño inventario: {size}')
    st.write(f'#### Precio medio del inventario: {mean}€')
    
    st.write(f'#### Top 10 artistas y sellos por recuento de items:')
    graph = graficazo()
    st.pyplot(graph)

def documentacion():
    st.write('### API')
    
    st.write('##### Validación app')
    st.write('El primer paso para la utilización de la api es la creación de una app en la: [web developer Discogs](https://www.discogs.com/es/settings/developers "web developer Discogs"). A continuación será necesario validar esta APP. Para mayor información de cómo validar la app ver el notebook [authorization](https://github.com/jvr0/AudioAlchemy/blob/main/notebooks/authorization.ipynb "authorization.ipynb"). A continuación la estructura de la variable auth:')
    st.write("```python\noauth = OAuth1(\n        key,\n        client_secret=secret,\n        resource_owner_key=access_oauth_token,\n        resource_owner_secret=access_oauth_token_secret,\n        verifier=oauth_verifier)")
    
    st.write('##### Endpoints')
    st.write('Los endpoints utilizados para este proyecto son aquellos relacionados con el manejo y actualización del inventario. A continuación los ejemplos de uso. Para más información sobre el uso de los endpoints: [SRC](https://github.com/jvr0/AudioAlchemy/blob/main/src/support_API.py "SRC")')
    
    if st.button('Autorización'):
        st.write("```python\nurl = 'https://api.discogs.com/oauth/identity'\nres = req.get(url, auth=oauth)``` ")
    
    if st.button('Solicitud inventario'):
        st.write("```python\nurl = 'https://api.discogs.com/inventory/export'\nres = req.post(url, auth=oauth)``` ")
    
    if st.button('Descarga último inventario'):
        st.write("```python\nurl = 'https://api.discogs.com/inventory/export'\nres = req.get(url, auth=oauth)\nurl_inv= res.json()['items'][-1]['download_url']\nres = req.get(url_inv, auth=oauth)\nzip_file = zipfile.ZipFile(io.BytesIO(res.content))\ncsv_file = zip_file.namelist()[0]\ncsv_data = zip_file.read(csv_file).decode('utf-8')``` ")
    
    if st.button('Actualización inventario'):
        st.write("```python\nurl = 'https://api.discogs.com/inventory/upload/change'\ncsv_file_path = '../data/upload.csv'\nfiles = {'upload': ('upload.csv', open(csv_file_path, 'rb'), 'text/csv')}\nres = req.post(url, auth=oauth, files=files)``` ")

    st.write('##### Formato Archivos')
    st.write("A la hora de la recepción y envío de archivos en la API se debe tener en cuenta lo siguiente:")
    st.write("1. El archivo recibido en el endpoint ```url = 'https://api.discogs.com/inventory/export'``` será un ZIP, por lo que es necesaria la librería ```zipfile``` para poder descomprimirlo y abrirlo.")
    st.write("2. El archivo enviado para actualizar archivos al endpoint ```url = 'https://api.discogs.com/inventory/upload/change'``` debe ser un csv que previamente haya sido abierto en nuestro código.")
    if st.button('Flujo de datos'):
        image = Image.open('../img/diagrama.png')
        st.image(image, use_column_width=True)
    
    st.write('### Producción')

# NAVEGACIÓN SIDEBAR

st.sidebar.title('AudioAlchemy')

if st.sidebar.button(':green[Repositorio]'):
        webbrowser.open_new_tab('https://github.com/jvr0/AudioAlchemy')

if st.sidebar.button(':blue[LinkedIn]'):
    webbrowser.open_new_tab('https://www.linkedin.com/in/joaquín-villaverde-roldán-4b9803230')

if st.sidebar.button(':grey[GitHub]'):
    webbrowser.open_new_tab('https://github.com/jvr0')

size = tamaño_inventario()
st.sidebar.write(f'### Tamaño inventario: {size}')

if st.sidebar.button(':orange[Pedir nuevo inventario a discogs]'):
    new = nuevo_inventario()
    st.sidebar.info(new)
    size = tamaño_inventario()

if st.sidebar.button(':orange[Preparar descarga inventario]'):
    descarga_inventario()
    csv_content = descarga_streamlit()    
    if csv_content:
        st.sidebar.download_button(label=':blue[Descargar inventario]', data=csv_content, file_name='inventario.csv', mime='text/csv')
        st.sidebar.info('Inventario descargado correctamente')
    else:
        st.sidebar.warning('Hubo un problema al descargar el inventario')

# Sidebar navigation
opciones = {
    "Inicio": pagina_inicio,
    "Estadísticas": statistics,
    "Documentacion": documentacion,
}

# Sidebar navigation selection
st.sidebar.write("## Navegación")
opcion_seleccionada = st.sidebar.radio("Ir a", list(opciones.keys()))

# Display the selected page
if opcion_seleccionada in opciones:
    opciones[opcion_seleccionada]()