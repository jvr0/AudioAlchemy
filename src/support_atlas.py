import streamlit as st
import pymongo
from pymongo import MongoClient

def connection():
    global collection

    uri = f"mongodb+srv://{st.secrets["usarname"]}:{st.secrets["pass"]}@{st.secrets["cluster_url"]}/"

    client = MongoClient(uri)

    db = client['Usuarios']

    collection = db['usuarios']

def nuevo_usuario(usuario, contraseña):
    user = {"joaquin": "Kingston7"}
    collection.insert_one(user)