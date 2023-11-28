import streamlit as st
import pandas as pd
from PIL import Image
import pylab as plt
import webbrowser
import base64
import io

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

st.sidebar.title('AudioAlchemy')

st.write('La siguiente página permité la actualización del inventario de ElArticoDiscos a través de la API discogs')

st.button('refrescar')


# SIDEBAR
st.sidebar.image(Image.open('../images/profile.jpg'))

url = 'https://www.discogs.com/es/user/ElArticoDiscos'
if st.sidebar.button('seller page'):
    webbrowser.open_new_tab(url)