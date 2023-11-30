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

# NAVEGACIÓN SIDEBAR

st.sidebar.title('AudioAlchemy')

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

# Sidebar navigation
opciones = {
    "Inicio": pagina_inicio,
    "Estadísticas": statistics,
}

# Sidebar navigation selection
st.sidebar.write("## Navegación")
opcion_seleccionada = st.sidebar.radio("Ir a", list(opciones.keys()))

# Display the selected page
if opcion_seleccionada in opciones:
    opciones[opcion_seleccionada]()