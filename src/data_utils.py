import pandas as pd
import json
import os
import streamlit as st
from src.draw_routes import cargar_rutas

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
def cargar_dataset(idioma, category_mapping):
    # Cargar el mapeo de columnas
    column_mappings = cargar_column_mappings()
    if not column_mappings:
        return pd.DataFrame()
    
    ruta_archivo = f"data/santiago_cabo_verde_recursos_{idioma}.csv"
    if os.path.exists(ruta_archivo):
        df = pd.read_csv(ruta_archivo)
        # Aplicar el mapeo de columnas
        df = df.rename(columns=column_mappings.get(idioma, {}))
        
        # Asignar category_id basado en el mapeo proporcionado
        if 'category' in df.columns:
            df['category_id'] = df['category'].map(category_mapping)
            df['category_id'] = df['category_id'].fillna('category_others')
        else:
            st.error("El dataset no contiene la columna 'category'.")
            df['category_id'] = 'category_others'
        
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

def filtrar_datos(datos, categorias_seleccionadas):
    if categorias_seleccionadas:
        datos = datos[datos['category_id'].isin(categorias_seleccionadas)]
    return datos

def inicializar_estado():
    if 'selected_resource_id' not in st.session_state:
        st.session_state['selected_resource_id'] = None
    if 'idioma_seleccionado' not in st.session_state:
        st.session_state['idioma_seleccionado'] = 'es' 
    if 'ruta_seleccionada' not in st.session_state:
        st.session_state['ruta_seleccionada'] = None
        
    # Idioma por defecto

def mostrar_logo():
    st.sidebar.image('assets/Logo_cabo_verde.png')

def seleccionar_idioma():
    idiomas_disponibles = obtener_idiomas()
    idioma_seleccionado = st.sidebar.selectbox(
        "Idioma:",
        idiomas_disponibles,
        index=idiomas_disponibles.index(st.session_state['idioma_seleccionado']) if 'idioma_seleccionado' in st.session_state else 0
    )
    st.session_state['idioma_seleccionado'] = idioma_seleccionado
    return idioma_seleccionado

def cargar_datos(idioma_seleccionado):
    traducciones = cargar_traducciones(idioma_seleccionado)
    category_mapping = traducciones.get("category_mapping", {})
    datos = cargar_dataset(idioma_seleccionado, category_mapping)
    return datos, traducciones

def seleccionar_categorias(traducciones, datos):
    categorias = datos[['category_id', 'category']].drop_duplicates().sort_values('category')
    categoria_dict = dict(zip(categorias['category'], categorias['category_id']))
    categorias_labels = list(categoria_dict.keys())
    categorias_seleccionadas_labels = st.sidebar.multiselect(
        traducciones.get("select_category", "Categorias:"),
        categorias_labels
    )
    categorias_seleccionadas_ids = [categoria_dict[label] for label in categorias_seleccionadas_labels]
    return categorias_seleccionadas_ids

def seleccionar_ruta(traducciones):
    rutas_df = cargar_rutas()
    ruta_predefinida = None
    if not rutas_df.empty:
        ruta_predefinida = st.sidebar.selectbox(
            traducciones.get("select_route", "Seleccionar ruta"),
            ['Ninguna'] + list(rutas_df['Nombre de la ruta'].unique())
        )
        st.session_state['ruta_seleccionada'] = ruta_predefinida
        if ruta_predefinida == 'Ninguna':
            ruta_predefinida = None
    return ruta_predefinida, rutas_df