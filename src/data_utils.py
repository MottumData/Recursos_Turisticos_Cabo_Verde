import pandas as pd
import json
import os
import streamlit as st
from src.draw_routes import cargar_dataset_rutas
from src.column_mappings import cargar_column_mappings

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

def filtrar_datos(datos, categorias_seleccionadas_ids=None, recurso_seleccionados_ids=None):
    if categorias_seleccionadas_ids and recurso_seleccionados_ids:
        datos_filtrados = datos[
            datos['category_id'].isin(categorias_seleccionadas_ids) |  # Operador OR
            datos['id'].isin(recurso_seleccionados_ids)
        ]
    elif categorias_seleccionadas_ids:
        datos_filtrados = datos[datos['categoria_id'].isin(categorias_seleccionadas_ids)]
    elif recurso_seleccionados_ids:
        datos_filtrados = datos[datos['id'].isin(recurso_seleccionados_ids)]
    else:
        datos_filtrados = datos
    return datos_filtrados

def inicializar_estado():
    if 'selected_resource_id' not in st.session_state:
        st.session_state['selected_resource_id'] = None
    if 'idioma_seleccionado' not in st.session_state:
        st.session_state['idioma_seleccionado'] = 'es' 
    if 'ruta_seleccionada' not in st.session_state:
        st.session_state['selected_route_id'] = None
        
    # Idioma por defecto

def mostrar_logo():
    st.image('assets/Logo_cabo_verde.png')

def seleccionar_idioma():
    idiomas_disponibles = obtener_idiomas()
    idioma_seleccionado = st.selectbox(
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

def cargar_datos_rutas(idioma_seleccionado):
    traducciones = cargar_traducciones(idioma_seleccionado)
    datos = cargar_dataset_rutas(idioma_seleccionado, traducciones.get("category_mapping_ruta", {}))
    return datos, traducciones

def seleccionar_categorias(traducciones, datos):
    categorias = datos[['category_id', 'category']].drop_duplicates().sort_values('category')
    categoria_dict = dict(zip(categorias['category'], categorias['category_id']))
    categorias_labels = list(categoria_dict.keys())
    categorias_seleccionadas_labels = st.multiselect(
        traducciones.get("select_category", "Categorias:"),
        categorias_labels
    )
    categorias_seleccionadas_ids = [categoria_dict[label] for label in categorias_seleccionadas_labels]
    return categorias_seleccionadas_ids


# src/data_utils.py

def seleccionar_ruta(traducciones):
    category_mapping_ruta = traducciones.get("category_mapping_ruta", {})
    rutas_df = cargar_dataset_rutas(st.session_state['idioma_seleccionado'], category_mapping_ruta)
    if not rutas_df.empty:
        ruta_options = ['Ninguna'] + list(rutas_df['route_name'].unique())
        selected_route_name = st.selectbox(
            traducciones.get("select_route", "Seleccionar ruta"),
            ruta_options
        )
        if selected_route_name != 'Ninguna':
            ruta = rutas_df[rutas_df['route_name'] == selected_route_name]
            if not ruta.empty:
                selected_route_id = ruta.iloc[0]['id']
            else:
                selected_route_id = None
        else:
            selected_route_id = None
    else:
        selected_route_name = 'Ninguna'
        selected_route_id = None

    # Almacenar el nombre de la ruta en st.session_state
    st.session_state['selected_route_name'] = selected_route_name
    st.session_state['selected_route_id'] = selected_route_id

    return selected_route_name, selected_route_id