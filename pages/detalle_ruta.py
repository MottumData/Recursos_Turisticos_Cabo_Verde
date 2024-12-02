import streamlit as st
import pandas as pd
from src.data_utils import cargar_traducciones
from src.draw_routes import cargar_dataset_rutas

def cargar_datos_ruta(idioma_seleccionado, route_id):
    traducciones = cargar_traducciones(idioma_seleccionado)
    category_mapping = traducciones.get("category_mapping_ruta", {})
    datos = cargar_dataset_rutas(idioma_seleccionado, category_mapping)
    if datos.empty:
        st.error("No hay datos disponibles para este idioma.")
        st.stop()
    ruta = datos[datos['id'] == route_id]
    if ruta.empty:
        st.error(f"Ruta no encontrada: {route_id}")
        st.stop()
    return ruta.iloc[0], traducciones

def mostrar_informacion_general(ruta, traducciones):
    st.subheader(traducciones.get('informacion_general', "Información General"))
    mostrar_informacion_basica(ruta, traducciones)
    mostrar_descripcion(ruta, traducciones)

def mostrar_informacion_basica(ruta, traducciones):
    info_basica = {
        traducciones.get("route_name_label", "Nombre de la Ruta"): ruta.get('route_name', ''),
        traducciones.get("distance_label", "Distancia"): ruta.get('distance', ''),
        traducciones.get("duration_label", "Duración"): ruta.get('duration', ''),
        traducciones.get("difficulty_label", "Dificultad"): ruta.get('difficulty', ''),
    }
    st.table(info_basica)

def mostrar_descripcion(ruta, traducciones):
    descripcion = ruta.get('description', '')
    if descripcion:
        st.markdown(f"**{traducciones.get('descripcion', 'Descripción')}:**")
        st.write(descripcion)

def mostrar_puntos_interes(ruta, traducciones):
    puntos_interes = ruta.get('points_of_interest', '')
    if puntos_interes:
        st.markdown(f"**{traducciones.get('puntos_interes', 'Puntos de Interés')}:**")
        st.write(puntos_interes)

def mostrar_recursos_asociados(ruta, traducciones):
    recursos_asociados = ruta.get('resources_included', '')
    if recursos_asociados:
        st.markdown(f"**{traducciones.get('recursos_asociados', 'Recursos Asociados')}:**")
        st.write(recursos_asociados)

def mostrar_informacion_adicional(ruta, traducciones):
    with st.expander(traducciones.get('informacion_adicional', 'Información Adicional')):
        mostrar_condiciones_climaticas(ruta, traducciones)
        mostrar_epoca_recomendada(ruta, traducciones)
        mostrar_tipos_transporte(ruta, traducciones)

def mostrar_condiciones_climaticas(ruta, traducciones):
    condiciones = ruta.get('weather_conditions', '')
    if condiciones:
        st.markdown(f"**{traducciones.get('condiciones_climaticas', 'Condiciones Climáticas')}:**")
        st.write(condiciones)

def mostrar_epoca_recomendada(ruta, traducciones):
    epoca = ruta.get('recommended_season', '')
    if epoca:
        st.markdown(f"**{traducciones.get('epoca_recomendada', 'Época Recomendada')}:**")
        st.write(epoca)

def mostrar_tipos_transporte(ruta, traducciones):
    transporte = ruta.get('transport_types', '')
    if transporte:
        st.markdown(f"**{traducciones.get('tipos_transporte', 'Tipos de Transporte')}:**")
        st.write(transporte)

def mostrar_accesibilidad(ruta, traducciones):
    with st.expander(traducciones.get('accesibilidad', 'Accesibilidad')):
        mostrar_acceso_inicio(ruta, traducciones)
        mostrar_acceso_final(ruta, traducciones)
        mostrar_medios_acceso(ruta, traducciones)

def mostrar_acceso_inicio(ruta, traducciones):
    acceso_inicio = ruta.get('start_access', '')
    if acceso_inicio:
        st.markdown(f"**{traducciones.get('acceso_inicio', 'Acceso al Inicio de la Ruta')}:**")
        st.write(acceso_inicio)

def mostrar_acceso_final(ruta, traducciones):
    acceso_final = ruta.get('end_access', '')
    if acceso_final:
        st.markdown(f"**{traducciones.get('acceso_final', 'Acceso al Final de la Ruta')}:**")
        st.write(acceso_final)

def mostrar_medios_acceso(ruta, traducciones):
    medios = ruta.get('access_means', '')
    if medios:
        st.markdown(f"**{traducciones.get('medios_acceso', 'Medios de Acceso')}:**")
        st.write(medios)

def mostrar_servicios(ruta, traducciones):
    with st.expander(traducciones.get('servicios', 'Servicios')):
        mostrar_servicios_disponibles(ruta, traducciones)
        mostrar_estado_senalizacion(ruta, traducciones)

def mostrar_servicios_disponibles(ruta, traducciones):
    servicios = ruta.get('available_services', '')
    if servicios:
        st.markdown(f"**{traducciones.get('servicios_disponibles', 'Servicios Disponibles')}:**")
        st.write(servicios)

def mostrar_estado_senalizacion(ruta, traducciones):
    senalizacion = ruta.get('signage_status', '')
    if senalizacion:
        st.markdown(f"**{traducciones.get('estado_senalizacion', 'Estado de la Señalización')}:**")
        st.write(senalizacion)

def mostrar_imagenes(ruta):
    imagenes = []
    for i in range(1, 5):
        img_key = f'image_{i}'
        img_url = ruta.get(img_key, '')
        if img_url and pd.notna(img_url):
            imagenes.append(img_url)
    if imagenes:
        st.subheader('Imágenes')
        st.image(imagenes, use_column_width=True)

def aplicar_css_personalizado():
    st.markdown("""
    <style>
        /* Estilo para los subtítulos */
        .stMarkdown h2{
            color: #2E586E;
            margin-top: 20px;
        }
        /* Estilo para los expanders */
        .streamlit-expanderHeader {
            font-size: 1.1em;
            color: #1F4E79;
            font-weight: bold;
        }
        /* Estilo para las tablas */
        .stTable {
            background-color: #F9F9F9;
        }
        /* Estilo para los textos */
        .stMarkdown p {
            font-size: 1em;
            color: #333333;
        }
        .stButton button {
            width: 100%; /* Ajustar al tamaño del sidebar */
            margin: 20px auto;
            margin-top: 5px;
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

# Configuración de la página
st.set_page_config(layout="wide", page_title="Detalle de la Ruta")
aplicar_css_personalizado()

st.sidebar.image('assets/Logo_cabo_verde.png')

# Obtener el ID de la ruta
route_id = st.session_state.get("route_id", None)
if route_id is None:
    st.error("No se proporcionó ningún ID de ruta.")
    st.stop()

# Obtener el idioma seleccionado
idioma_seleccionado = st.session_state.get('idioma_seleccionado', 'es')

# Cargar los datos de la ruta
ruta, traducciones = cargar_datos_ruta(idioma_seleccionado, route_id)

# Título de la página
st.title(f"{ruta['id']}")

# Columnas para el diseño
cols = st.columns([3, 2])

with cols[0]:
    mostrar_informacion_general(ruta, traducciones)
    mostrar_puntos_interes(ruta, traducciones)
    mostrar_recursos_asociados(ruta, traducciones)
    mostrar_informacion_adicional(ruta, traducciones)
    mostrar_accesibilidad(ruta, traducciones)
    mostrar_servicios(ruta, traducciones)

#with cols[1]:
    #mostrar_imagenes(ruta)

# Botón para regresar a la página principal
if st.sidebar.button(traducciones.get('volver_al_mapa', 'Volver al Mapa')):
    st.switch_page("app.py")