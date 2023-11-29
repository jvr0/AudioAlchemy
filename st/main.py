import streamlit as st
import pandas as pd
import schedule
import time
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
    initial_sidebar_state="collapsed",
)

# MURO

st.title('AudioAlchemy')

size = tamaño_inventario()
st.write(f'### Tamaño inventario: {size}')

if st.button('identificación'):
    user = autentificacion()
    st.info(user)

if st.button('Pedir nuevo inventario a discogs'):
    new = nuevo_inventario()
    st.info(new)

def activar_programacion(dias, hora): # Programar la ejecución de la función en un horario específico
    for dia in dias:
        schedule.every().day.at(f"{hora:02d}:00").do(mi_funcion).tag(f"{dia}-{hora}")
    return f'Programación activa'

def cancelar_programacion(): # Cancelar todas las tareas programadas
    schedule.clear()
    return f'Programación cancelada'

# Widget para seleccionar los días de la semana
dias = st.multiselect("Selecciona los días de la semana (multiselección)", 
                              ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'])
# Widget para seleccionar la hora
hora = st.slider("Selecciona la hora", 0, 23, 9)  # Valores de 0 a 23 para las horas

# Botón personalizado Uno al lado del otro
button_html = """
    <style>
        .my-custom-btn {
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-size: 1rem;
            cursor: pointer;
            border: none;
            margin-right: 10px;
        }
        .green-btn {
            background-color: #00CC66;
            color: white;
        }
        .red-btn {
            background-color: #ff6b6b;
            color: white;
        }
    </style>
    <div>
        <button class="my-custom-btn green-btn" type="button" onclick="programar()">Programar</button>
        <button class="my-custom-btn red-btn" type="button" onclick="cancelar()">Cancelar</button>
    </div>
    <script>
        function programar() {
            const diasSeleccionados = document.querySelector('[aria-label="Selecciona los días de la semana (multiselección)"]').value;
            const horaSeleccionada = document.querySelector('[aria-label="Selecciona la hora"]').value;
            const diasArray = diasSeleccionados ? diasSeleccionados.split(',') : [];
            const hora = parseInt(horaSeleccionada);

            if (diasArray.length > 0 && !isNaN(hora)) {
                const payload = {
                    dias: diasArray,
                    hora: hora
                };
                const command = "horario(" + JSON.stringify(payload) + ")";
                Streamlit.CommandQueue.getStreamlitIO().sendCommand(command);
            } else {
                alert("Por favor selecciona al menos un día y una hora.");
            }
        }
        
        function cancelar() {
            Streamlit.CommandQueue.getStreamlitIO().sendCommand("cancelar_programacion()");
        }
    </script>
"""

# Mostrar los botones personalizados
if st.markdown(button_html, unsafe_allow_html=True):
    activar_programacion(dias, hora)

# SIDEBAR

st.sidebar.write('El siguiente proyecto consiste en un encargo realizado por la compañía de venta online [El Ártico Discos](https://www.discogs.com/es/seller/elarticodiscos/profile "El Ártico Discos"). Se ha propuesto un trabajo de ingeniería para la actualización automática del inventario. El objetivo es mejorar la ubicación de los items dentro de la plataforma [Discogs](https://www.discogs.com/es/ "Discogs").')

st.sidebar.image(Image.open('../img/profile.jpg'))

