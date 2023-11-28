import streamlit as st
import pandas as pd
from PIL import Image
import pylab as plt
import webbrowser
import base64
import io

import sys
sys.path.append('../src')
from support import *

page_bg_img = '''
                <style>
                body {
                background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
                background-size: cover;
                }
                </style>
                '''
st.markdown(page_bg_img, unsafe_allow_html=True)


# MURO

st.title('AudioAlchemy')

if st.button('identificación'):
    user = autentificacion()
    st.info(user)

# SIDEBAR

st.sidebar.write('El siguiente proyecto consiste en un encargo realizado por la compañía de venta online [El Ártico Discos](https://www.discogs.com/es/seller/elarticodiscos/profile "El Ártico Discos"). Se ha propuesto un trabajo de ingeniería para la actualización automática del inventario. El objetivo es mejorar la ubicación de los items dentro de la plataforma [Discogs](https://www.discogs.com/es/ "Discogs").')


url = 'https://www.discogs.com/es/user/ElArticoDiscos'
if st.sidebar.button('seller page'):
    webbrowser.open_new_tab(url)

st.sidebar.image(Image.open('../images/profile.jpg'))
