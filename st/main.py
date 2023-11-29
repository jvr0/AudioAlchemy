import streamlit as st
import pandas as pd
from PIL import Image
import pylab as plt
import webbrowser
import base64
import io

import sys
sys.path.append('../src')
from support_API import *
from support_st import *

# MURO

st.title('AudioAlchemy')

size = tamaño_inventario()
st.write(f'### Tamaño inventario: {size}')

if st.button('identificación'):
    user = autentificacion()
    st.info(user)

# SIDEBAR

st.sidebar.write('El siguiente proyecto consiste en un encargo realizado por la compañía de venta online [El Ártico Discos](https://www.discogs.com/es/seller/elarticodiscos/profile "El Ártico Discos"). Se ha propuesto un trabajo de ingeniería para la actualización automática del inventario. El objetivo es mejorar la ubicación de los items dentro de la plataforma [Discogs](https://www.discogs.com/es/ "Discogs").')

st.sidebar.image(Image.open('../img/profile.jpg'))

