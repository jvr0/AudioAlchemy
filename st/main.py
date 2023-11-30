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

    paquete = st.number_input("Ingresa el tamaño del paquete a enviar",
                                value=0,
                                min_value=0,
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

    # Widget para seleccionar los días de la semana
    dias = st.multiselect("Selecciona los días de la semana (multiselección)", ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'])

    # Widget para seleccionar la hora
    hora = st.slider("Selecciona la hora", 0, 23, 9)  # Valores de 0 a 23 para las horas

    programacion_activa = False


    def activar_programacion(dias, hora, paquete):
        global programacion_activa
        for dia in dias:
            schedule.every().day.at(f"{hora:02d}:05").do(lanzamiento_programado, paquete).tag(f"{dia}-{hora}")

    def cancelar_programacion():
        global programacion_activa
        schedule.clear()

    if st.button(":green[Programar]"):
        activar_programacion(dias, hora, paquete)
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
            time.sleep(1)
        else:
            time.sleep(1)


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

    


# NAVEGACIÓN SIDEBAR

st.sidebar.title('AudioAlchemy')

# Crear un menú para cambiar entre páginas
opciones = {
    "Inicio": pagina_inicio,
    "Estadísticas": statistics,
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
    st.sidebar.info(new)
    size = tamaño_inventario()

if st.sidebar.button('Preparar descarga inventario'):
    descarga_inventario()
    csv_content = descarga_streamlit()    
    if csv_content:
        st.sidebar.download_button(label=':blue[Descargar inventario]', data=csv_content, file_name='inventario.csv', mime='text/csv')
        st.sidebar.info('Inventario descargado correctamente')
    else:
        st.sidebar.warning('Hubo un problema al descargar el inventario')