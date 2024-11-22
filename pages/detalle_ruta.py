# FILE: pages/detalle_ruta.py

import streamlit as st
import pandas as pd
from src.data_utils import cargar_dataset, cargar_traducciones, obtener_idiomas, cargar_rutas

# Configura la página para que use el diseño ancho y un título específico
st.set_page_config(layout="wide", page_title="Detalle de la Ruta")

st.sidebar.image('assets/Logo_cabo_verde.png')
# Obtener los parámetros de la URL
route_id = st.session_state.get("route_id", [None])

if route_id is None:
    st.error("No se proporcionó ningún ID de ruta.")
    st.stop()

# Obtener el idioma seleccionado del session_state
idioma_seleccionado = st.session_state.get('idioma_seleccionado', 'es')  # 'es' por defecto

# Cargar las traducciones para el idioma seleccionado
traducciones = cargar_traducciones(idioma_seleccionado)

# Cargar el dataset de rutas
rutas_df = cargar_rutas()

if rutas_df.empty:
    st.error("No hay datos disponibles para este idioma.")
    st.stop()

# Encontrar la ruta por route_id
ruta = rutas_df[rutas_df['Nombre de la ruta'] == route_id]

if ruta.empty:
    st.error("Ruta no encontrada.")
    st.stop()

ruta = ruta.iloc[0]  # Convertir a Series

st.title(f"Detalles de: {ruta['Nombre de la ruta']}")

cols = st.columns([3, 2])

with cols[0]:
    # Información básica
    info_basica = {
        traducciones.get("municipios_label", "Municipios"): ruta.get('Municipios por los que transcurre', ''),
        traducciones.get("duracion_label", "Duración"): ruta.get('Duración', ''),
        traducciones.get("distancia_label", "Distancia"): ruta.get('Distancia', ''),
        traducciones.get("modo_acceso_label", "Modo de acceso"): ruta.get('Modo de acceso', ''),
        traducciones.get("dificultad_label", "Dificultad"): ruta.get('Dificultad', ''),
        traducciones.get("actividad_label", "Actividad"): ruta.get('Actividad', ''),
        traducciones.get("recursos_incluidos_label", "Recursos incluidos"): ruta.get('Recursos incluidos', ''),
        traducciones.get("punto_inicio_label", "Punto de inicio"): ruta.get('Punto de inicio', ''),
        traducciones.get("punto_salida_label", "Punto de salida"): ruta.get('Punto de salida', '')
    }

    for key, value in info_basica.items():
        if value:
            st.markdown(f"**{key}:** {value}")
    
    # Descripción de la ruta
    descripcion = ruta.get('Descripción de la ruta', '')
    if descripcion:
        st.markdown(f"### {traducciones.get('descripcion', 'Descripción')}")
        st.info(descripcion)

with cols[1]:
    # Mostrar imágenes si están disponibles
    for i in range(1, 5):
        img_key = f'Imagen {i}'
        img_url = ruta.get(img_key, '')
        if img_url and pd.notna(img_url):
            st.image(img_url, use_container_width=True)    

col1b, col2b, col3b = st.columns([1, 2, 1])
# Botón para regresar a la página principal
with col2b:
    if st.button("Volver al Mapa"):
        # Navegar de regreso a la página principal sin parámetros de consulta
        st.experimental_set_query_params()
        st.experimental_rerun()

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