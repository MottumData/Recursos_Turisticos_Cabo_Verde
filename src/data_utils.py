import pandas as pd
import json
import os
import streamlit as st

@st.cache_data
def cargar_column_mappings():
    # Obtener la ruta absoluta del archivo JSON
    ruta = os.path.join(os.path.dirname(__file__), "column_mappings.json")
    
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            mappings = json.load(f)
        return mappings
    else:
        st.error("El archivo column_mappings.json no existe.")
        return {}

@st.cache_data
def cargar_dataset(idioma):
    # Cargar el mapeo de columnas
    column_mappings = cargar_column_mappings()
    if not column_mappings:
        return pd.DataFrame()
    
    ruta_archivo = f"data/santiago_cabo_verde_recursos_{idioma}.csv"
    if os.path.exists(ruta_archivo):
        df = pd.read_csv(ruta_archivo)
        # Aplicar el mapeo de columnas
        df = df.rename(columns=column_mappings.get(idioma, {}))
        return df
    else:
        st.error(f"El archivo para el idioma {idioma} no existe.")
        return pd.DataFrame()

def cargar_traducciones(idioma):
    ruta = os.path.join("traducciones", f"{idioma}.json")
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            traducciones = json.load(f)
        return traducciones
    else:
        st.error(f"El archivo de traducciones para {idioma} no existe.")
        return {}

def obtener_idiomas():
    return [archivo.split(".")[0] for archivo in os.listdir("traducciones") if archivo.endswith(".json")]