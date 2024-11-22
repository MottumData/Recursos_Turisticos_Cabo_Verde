# FILE: pages/detalle_recurso.py

import streamlit as st
import pandas as pd
from src.data_utils import cargar_dataset, cargar_traducciones, obtener_idiomas

# Configura la página para que use el diseño ancho y un título específico
st.set_page_config(layout="wide", page_title="Detalle del Recurso")

st.sidebar.image('assets/Logo_cabo_verde.png')
# Obtener los parámetros de la URL
resource_id = st.session_state.get("resource_id", [None])

if resource_id is None:
    st.error("No se proporcionó ningún ID de recurso.")
    st.stop()

# Obtener el idioma seleccionado del session_state
idioma_seleccionado = st.session_state.get('idioma_seleccionado', 'es')  # 'es' por defecto

# Cargar las traducciones para el idioma seleccionado
traducciones = cargar_traducciones(idioma_seleccionado)

category_mapping = traducciones.get("category_mapping", {})

# Cargar el dataset correspondiente y aplicar el mapeo de columnas
datos = cargar_dataset(idioma_seleccionado, category_mapping)

if datos.empty:
    st.error("No hay datos disponibles para este idioma.")
    st.stop()

# Encontrar el recurso por resource_id
recurso = datos[datos['id'] == resource_id]

if recurso.empty:
    st.error("Recurso no encontrado.")
    st.stop()

recurso = recurso.iloc[0]  # Convertir a Series

st.title(f"Detalles de: {recurso['resource_name']}")

cols = st.columns([3, 2])

with cols[0]:
    # Información básica
    info_basica = {
        traducciones.get("council_label", "Consejo"): recurso.get('council', ''),
        traducciones.get("parish_label", "Parroquia"): recurso.get('parish', ''),
        traducciones.get("classification_label", "Clasificación"): recurso.get('classification', ''),
        traducciones.get("village_label", "Aldea"): recurso.get('village', ''),
        traducciones.get("neighborhood_label", "Vecindario"): recurso.get('neighborhood', '')
    }

    for key, value in info_basica.items():
        if value:
            st.markdown(f"**{key}:** {value}")
    
    # Descripción del producto
    descripcion = recurso.get('description', '')
    if descripcion:
        st.markdown(f"### {traducciones.get('descripcion', 'Descripción')}")
        st.info(descripcion)
    
    # Elementos materiales asociados
    elementos_materiales = recurso.get('material_elements', '')
    if elementos_materiales:
        st.markdown(f"### {traducciones.get('elementos_materiales', 'Elementos Materiales')}")
        st.info(elementos_materiales)
    
    # Elementos naturales asociados
    elementos_naturales = recurso.get('natural_elements', '')
    if elementos_naturales:
        st.markdown(f"### {traducciones.get('elementos_naturales', 'Elementos Naturales')}")
        st.info(elementos_naturales)

with cols[1]:
    # Mostrar imágenes si están disponibles
    for i in range(1, 5):
        img_key = f'feature_image_{i}'
        img_url = recurso.get(img_key, '')
        if img_url and pd.notna(img_url):
            st.image(img_url, use_container_width=True)    

col1b, col2b, col3b = st.columns([1, 2, 1])
# Botón para regresar a la página principal
with col2b:
    if st.sidebar.button("Volver al Mapa"):
        # Navegar de regreso a la página principal sin parámetros de consulta
        st.switch_page("app.py")
        st.rerun()

# CSS personalizado
st.markdown("""
    <style>
        .stColumn {
            padding-left: 30px;
            padding-right: 30px;
            padding-top: 10px;
        }
        .stExpander {
            padding-left: 20px;
            padding-right: 20px;
        }
        .stButton button {
            width: 100%; /* Ajustar al tamaño del sidebar */
            margin: 20px auto;
            margin-top: 20px;
            padding: 8px 24px;
            border-radius: 3px;
            box-shadow: 0px 0px 12px -2px rgba(0,0,0,0.5);
            line-height: 1.25;
            background: #FC6E51;
            text-decoration: none;
            user-select: none;
            color: white;
            font-size: 16px;
            letter-spacing: .08em;
            position: relative;
            transition: background-color .6s ease;
            overflow: hidden;
        }
        .stButton button:after {
            content: "";
            position: absolute;
            width: 0;
            height: 0;
            top: 50%;
            left: 50%;
            transform-style: flat;
            transform: translate3d(-50%,-50%,0);
            background: rgba(255, 255, 255, 0.1);
            border-radius: 100%;
            transition: width .3s ease, height .3s ease;
        }
        .stButton button:focus,
        .stButton button:hover {
            background: #E65A3E;
            color: white !important;
        }
        .stButton button:active:after {
            width: 300px;
            height: 300px;
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
        .stAppHeader {
            display: none;
        }
        .stAppToolbar {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)