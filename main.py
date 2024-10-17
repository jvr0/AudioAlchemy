import streamlit as st
import pandas as pd
import schedule
import time
from PIL import Image
import webbrowser
import base64
import io

from src.support_API import *
from src.support_st import *

# CONFIG INICIAL
st.set_page_config(
    page_title="AudioAlchemy",
    page_icon=":alembic:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Contraseña para acceder a la aplicación
password = st.secrets['password']  # contraseña

# Pide al usuario que ingrese la contraseña
password_placeholder = st.empty()
user_input = password_placeholder.text_input("Ingresa la contraseña:", type="password")

# Verifica si la contraseña ingresada es correcta
if user_input == password:
    # Elimina la celda de la contraseña si la contraseña es correcta
    password_placeholder.empty()
    size = tamaño_inventario_venta()

    if 'programacion_activa' not in st.session_state:
        st.session_state['programacion_activa'] = False    

    # MURO 
    st.write(f'## Programar actualización')

    # Widget para seleccionar la hora
    hora = st.slider("Selecciona la hora", 0, 23, 9)  # Valores de 0 a 23 para las horas

    def activar_programacion(hora):
        schedule.every().day.at(f"{hora:02d}:00").do(lanzamiento_programado).tag(f"{hora}")
        st.session_state['programacion_activa'] = True

    def cancelar_programacion():
        schedule.clear()
        st.session_state['programacion_activa'] = False

    if st.button(":green[Programar]"):
        activar_programacion(hora)

    if st.button(":red[Cancelar]"):
        cancelar_programacion()

    st.write(schedule.get_jobs())

    if st.session_state['programacion_activa']:
        st.write(f':green[Estado de la programación: {st.session_state["programacion_activa"]}]')
    else:
        st.write(f':red[Estado de la programación: {st.session_state["programacion_activa"]}]')

    # Esta sección debería ser manejada en un thread separado o usando async programming
    # ya que puede hacer que Streamlit se congele.
    while st.session_state['programacion_activa']:
        schedule.run_pending()
        time.sleep(2)

    icono = Image.open('img/icono.png')
    st.sidebar.image(icono, width=100)

    st.sidebar.write('---')

    size = tamaño_inventario_venta()
    st.sidebar.write(f'### Tamaño inventario: {size}')

    # CONTROL DEL INVENTARIO
    if st.sidebar.button('Pedir nuevo inventario a discogs'):
        new = nuevo_inventario()
        st.sidebar.info(new)

    if st.sidebar.button('Preparar descarga inventario'):
        descarga_inventario()
        csv_content = descarga_streamlit()    
        size = tamaño_inventario_venta()
        st.sidebar.write(f'### Tamaño actualizado {size}')
        if csv_content:
            st.sidebar.download_button(label=':blue[Descargar inventario]', data=csv_content, file_name='inventario.csv', mime='text/csv')
            st.sidebar.info('Inventario descargado correctamente')
        else:
            st.sidebar.warning('Hubo un problema al descargar el inventario')

    st.sidebar.write('---')

    # LINKS
    st.sidebar.write('---')
    if st.sidebar.button(':blue[Personal Links]'):
        st.sidebar.write('https://github.com/jvr0')
        st.sidebar.write('https://www.linkedin.com/in/joaquín-villaverde-roldán-4b9803230')
        st.sidebar.write('https://github.com/jvr0/AudioAlchemy')

elif user_input != "" and user_input != password:
    st.error("Contraseña incorrecta. Por favor, intenta nuevamente.")
