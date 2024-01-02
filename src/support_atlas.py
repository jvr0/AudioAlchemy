import streamlit as st
import pymongo
from pymongo import MongoClient

username = st.secrets['username']
password = st.secrets['pass']
cluster_url = st.secrets['cluster_url']


def connection():
    global collection

    uri = f"mongodb+srv://{username}:{password}@{cluster_url}/"

    client = MongoClient(uri)

    db = client['Usuarios']

    collection = db['usuarios']
    
    return collection

def nuevo_usuario(usuario, contraseña):
    user = {"joaquin": "Kingston7"}
    collection.insert_one(user)