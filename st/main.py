import streamlit as st
import pandas as pd
import schedule
import time
import subprocess
from PIL import Image
import pylab as plt
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


def pagina_inicio():
    # MURO

    # ACTUALIZAR AHORA

    st.write(f'### Actualizar ahora')
    paquete = st.number_input("Ingresa el tamaño del paquete a enviar",
                                value=0,
                                min_value=0,
                                max_value=size,
                                step=1)
    st.write(f"El paquete que se enviará es de: {paquete}")

    if st.button(':green[Actualizar ahora]'):
        paquete = int(paquete)
        user = lanzamiento(paquete)
        st.info(user)

    # PROGRAMAR ACTUALIZACIÓN

    st.write(f'### Programar actualización')

    # Widget para seleccionar los días de la semana
    dias = st.multiselect("Selecciona los días de la semana (multiselección)", ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'])

    # Widget para seleccionar la hora
    hora = st.slider("Selecciona la hora", 0, 23, 9)  # Valores de 0 a 23 para las horas

    programacion_activa = False

    def activar_programacion(dias, hora):
        global programacion_activa
        for dia in dias:
            schedule.every().day.at(f"{hora:02d}:00").do(autentificacion).tag(f"{dia}-{hora}")
        programacion_activa = True

    def cancelar_programacion():
        global programacion_activa
        schedule.clear()
        programacion_activa = False

    # Botones para programar y cancelar
    if st.button(":green[Programar]"):
        if dias:
            activar_programacion(dias, hora)
            st.info('Programación activada')
        else:
            st.warning('Por favor, selecciona al menos un día.')

    if st.button(":red[Cancelar]"):
        cancelar_programacion()
        st.info('Programación cancelada')

    # Mostrar estado de la programación
    if programacion_activa:
        st.info('Programación activa')


def statistics():
    df = df = pd.read_csv('../data/inventario.csv')
    df = df[df.status == 'For Sale']

    st.title("Estadísticas")

    size = tamaño_inventario()
    st.write(f'## Tamaño inventario: {size}')

    mean = round(df.price.mean(),2)
    st.write(f'## Media precio inventario: {mean}')

    artista = df.artist.value_counts().nlargest(2).index[-1]
    artista_valor = df.artist.value_counts()[1]
    st.write(f'## Artista más numeroso: {artista} {artista_valor}, items')

    


# SIDEBAR

st.sidebar.title('AudioAlchemy')

# Crear un menú para cambiar entre páginas
opciones = {
    "Inicio": pagina_inicio,
    "statistics": statistics,
}
st.sidebar.write("## Navegación")
opcion_seleccionada = st.sidebar.radio("Ir a", list(opciones.keys()))


# CONTENIDO SIDEBAR

# Mostrar la página seleccionada
if opcion_seleccionada in opciones:
    opciones[opcion_seleccionada]()

st.sidebar.write('El siguiente proyecto consiste en un encargo realizado por la compañía de venta online [El Ártico Discos](https://www.discogs.com/es/seller/elarticodiscos/profile "El Ártico Discos"). Se ha propuesto un trabajo de ingeniería para la actualización automática del inventario. El objetivo es mejorar la ubicación de los items dentro de la plataforma [Discogs](https://www.discogs.com/es/ "Discogs").')

size = tamaño_inventario()
st.sidebar.write(f'### Tamaño inventario: {size}')

if st.sidebar.button('Pedir nuevo inventario a discogs'):
    new = nuevo_inventario()
    st.info(new)

if st.sidebar.button('Preparar descarga inventario'):
    csv_content = descarga_streamlit()    
    if csv_content:
        st.sidebar.download_button(label=':blue[Descargar inventario]', data=csv_content, file_name='inventario.csv', mime='text/csv')
        st.sidebar.info('Inventario descargado correctamente')
    else:
        st.sidebar.warning('Hubo un problema al descargar el inventario')