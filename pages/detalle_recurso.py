import streamlit as st
import pandas as pd
from src.data_utils import cargar_dataset, cargar_traducciones, obtener_idiomas

def cargar_datos_recurso(idioma_seleccionado, resource_id):
    traducciones = cargar_traducciones(idioma_seleccionado)
    category_mapping = traducciones.get("category_mapping", {})
    datos = cargar_dataset(idioma_seleccionado, category_mapping)
    if datos.empty:
        st.error("No hay datos disponibles para este idioma.")
        st.stop()
    recurso = datos[datos['id'] == resource_id]
    if recurso.empty:
        st.error("Recurso no encontrado.")
        st.stop()
    return recurso.iloc[0], traducciones

def mostrar_informacion_general(recurso, traducciones):
    st.subheader(traducciones.get('informacion_general', "Información General"))
    mostrar_informacion_basica(recurso, traducciones)
    mostrar_descripcion(recurso, traducciones)
    mostrar_elementos_asociados(recurso, traducciones)

def mostrar_informacion_basica(recurso, traducciones):
    info_basica = {
        traducciones.get("island_label", "Isla"): recurso.get('island', ''),
        traducciones.get("council_label", "Consejo"): recurso.get('council', ''),
        traducciones.get("parish_label", "Parroquia"): recurso.get('parish', ''),
        traducciones.get("village_label", "Aldea"): recurso.get('village', ''),
        traducciones.get("neighborhood_label", "Vecindario"): recurso.get('neighborhood', ''),
        traducciones.get("classification_label", "Clasificación"): recurso.get('classification', '')
    }
    st.table(info_basica)

def mostrar_descripcion(recurso, traducciones):
    descripcion = recurso.get('description', '')
    if descripcion:
        st.markdown(f"**{traducciones.get('descripcion', 'Descripción')}:**")
        st.write(descripcion)

def mostrar_elementos_asociados(recurso, traducciones):
    elementos_materiales = recurso.get('material_elements', '')
    elementos_naturales = recurso.get('natural_elements', '')
    if elementos_materiales or elementos_naturales:
        st.markdown(f"**{traducciones.get('elementos_asociados', 'Elementos Asociados')}:**")
        if elementos_materiales:
            st.write(f"- {traducciones.get('elementos_materiales', 'Elementos Materiales')}: {elementos_materiales}")
        if elementos_naturales:
            st.write(f"- {traducciones.get('elementos_naturales', 'Elementos Naturales')}: {elementos_naturales}")

def mostrar_caracteristicas_recurso(recurso, traducciones):
    with st.expander(traducciones.get('caracteristicas_recurso', 'Características del Recurso')):
        mostrar_datos_pendientes(recurso, traducciones)
        mostrar_singularidad(recurso, traducciones)
        mostrar_satisfaccion_cliente(recurso, traducciones)
        mostrar_posibilidades_exploracion(recurso, traducciones)
        mostrar_intervenciones_necesarias(recurso, traducciones)

def mostrar_datos_pendientes(recurso, traducciones):
    datos_pendientes = recurso.get('pending_data', '')
    if datos_pendientes:
        st.markdown(f"**{traducciones.get('datos_pendientes', 'Datos Pendientes de Interés Turístico')}:**")
        st.write(datos_pendientes)

def mostrar_singularidad(recurso, traducciones):
    singularidad = recurso.get('uniqueness', '')
    if singularidad:
        st.markdown(f"**{traducciones.get('singularidad', 'Singularidad')}:**")
        st.write(singularidad)

def mostrar_satisfaccion_cliente(recurso, traducciones):
    satisfaccion = recurso.get('customer_satisfaction', '')
    if satisfaccion:
        st.markdown(f"**{traducciones.get('satisfaccion_cliente', 'Satisfacción del Cliente')}:**")
        st.write(satisfaccion)

def mostrar_posibilidades_exploracion(recurso, traducciones):
    exploracion = recurso.get('future_exploration', '')
    if exploracion:
        st.markdown(f"**{traducciones.get('exploracion_futura', 'Posibilidades de Exploración Futura')}:**")
        st.write(exploracion)

def mostrar_intervenciones_necesarias(recurso, traducciones):
    intervenciones = recurso.get('required_interventions', '')
    if intervenciones:
        st.markdown(f"**{traducciones.get('intervenciones_necesarias', 'Intervenciones Necesarias')}:**")
        st.write(intervenciones)

def mostrar_accesibilidad_y_senalizacion(recurso, traducciones):
    with st.expander(traducciones.get('accesibilidad_y_senalizacion', 'Accesibilidad y Señalización')):
        mostrar_acceso_recurso(recurso, traducciones)
        mostrar_acceso_tierra(recurso, traducciones)
        mostrar_acceso_maritimo(recurso, traducciones)
        mostrar_acceso_aereo(recurso, traducciones)
        mostrar_medios_viaje(recurso, traducciones)
        mostrar_senalizacion(recurso, traducciones)

def mostrar_acceso_recurso(recurso, traducciones):
    acceso = recurso.get('resource_access', '')
    if acceso:
        st.markdown(f"**{traducciones.get('acceso_recurso', 'Acceso al Recurso')}:** {acceso}")

def mostrar_acceso_tierra(recurso, traducciones):
    acceso_tierra = recurso.get('resource_access_land', '')
    if acceso_tierra:
        st.write(f"- **{traducciones.get('acceso_tierra', 'Acceso por Tierra')}:** {acceso_tierra}")

def mostrar_acceso_maritimo(recurso, traducciones):
    acceso_maritimo = recurso.get('resource_access_maritime', '')
    if acceso_maritimo:
        st.write(f"- **{traducciones.get('acceso_maritimo', 'Acceso Marítimo')}:** {acceso_maritimo}")

def mostrar_acceso_aereo(recurso, traducciones):
    acceso_aereo = recurso.get('resource_access_airborne', '')
    if acceso_aereo:
        st.write(f"- **{traducciones.get('acceso_aereo', 'Acceso Aéreo')}:** {acceso_aereo}")

def mostrar_medios_viaje(recurso, traducciones):
    medios_viaje = recurso.get('means_of_travel', '')
    if medios_viaje:
        st.write(f"- **{traducciones.get('medios_viaje', 'Medios de Viaje')}:** {medios_viaje}")

def mostrar_senalizacion(recurso, traducciones):
    senalizacion = {
        traducciones.get('senalizacion_dentro', 'Dentro del Municipio'): recurso.get('signage_within', ''),
        traducciones.get('senalizacion_fuera', 'Fuera del Municipio'): recurso.get('signage_outside', ''),
        traducciones.get('senalizacion_cerca', 'Cerca'): recurso.get('signage_nearby', '')
    }
    if any(senalizacion.values()):
        st.markdown(f"**{traducciones.get('senalizacion', 'Señalización')}:**")
        for key, value in senalizacion.items():
            if value:
                st.write(f"- {key}: {value}")

def mostrar_servicios_y_estado(recurso, traducciones):
    with st.expander(traducciones.get('servicios_y_estado', 'Servicios y Estado')):
        mostrar_servicios_basicos(recurso, traducciones)
        mostrar_servicios_turisticos(recurso, traducciones)
        mostrar_tipo_renta(recurso, traducciones)
        mostrar_estado_conservacion(recurso, traducciones)
        mostrar_nivel_uso(recurso, traducciones)

def mostrar_servicios_basicos(recurso, traducciones):
    servicios_basicos_fuera = recurso.get('basic_services_outside', '')
    servicios_basicos_dentro = recurso.get('basic_services_within', '')
    if servicios_basicos_fuera or servicios_basicos_dentro:
        st.markdown(f"**{traducciones.get('servicios_basicos', 'Servicios Básicos')}:**")
        if servicios_basicos_fuera:
            st.write(f"- {traducciones.get('servicios_basicos_fuera', 'Fuera del Recurso Turístico')}: {servicios_basicos_fuera}")
        if servicios_basicos_dentro:
            st.write(f"- {traducciones.get('servicios_basicos_dentro', 'Dentro del Recurso Turístico')}: {servicios_basicos_dentro}")

def mostrar_servicios_turisticos(recurso, traducciones):
    servicios_fuera = recurso.get('other_tourist_services_outside', '')
    servicios_dentro = recurso.get('other_tourist_services_within', '')
    if servicios_fuera or servicios_dentro:
        st.markdown(f"**{traducciones.get('servicios_turisticos', 'Servicios Turísticos')}:**")
        if servicios_fuera:
            st.write(f"- {traducciones.get('servicios_fuera', 'Fuera del Recurso Turístico')}: {servicios_fuera}")
        if servicios_dentro:
            st.write(f"- {traducciones.get('servicios_dentro', 'Dentro del Recurso Turístico')}: {servicios_dentro}")

def mostrar_tipo_renta(recurso, traducciones):
    tipo_renta = recurso.get('type_of_income', '')
    if tipo_renta:
        st.markdown(f"**{traducciones.get('tipo_renta', 'Tipo de Renta')}:** {tipo_renta}")

def mostrar_estado_conservacion(recurso, traducciones):
    estado_conservacion = recurso.get('conservation_status', '')
    if estado_conservacion:
        st.markdown(f"**{traducciones.get('estado_conservacion', 'Estado de Conservación')}:** {estado_conservacion}")

def mostrar_nivel_uso(recurso, traducciones):
    nivel_uso = recurso.get('current_level_of_usage', '')
    if nivel_uso:
        st.markdown(f"**{traducciones.get('nivel_uso', 'Nivel Actual de Uso')}:** {nivel_uso}")

def mostrar_imagenes(recurso):
    imagenes = []
    for i in range(1, 5):
        img_key = f'feature_image_{i}'
        img_url = recurso.get(img_key, '')
        if img_url and pd.notna(img_url):
            imagenes.append(img_url)
    if imagenes:
        st.subheader(traducciones.get('imagenes', 'Imágenes'))
        st.image(imagenes, use_container_width=True)

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
st.set_page_config(layout="wide", page_title="Detalle del Recurso")
aplicar_css_personalizado()

st.sidebar.image('assets/Logo_cabo_verde.png')

# Obtener el ID del recurso
resource_id = st.session_state.get("resource_id", None)
if resource_id is None:
    st.error("No se proporcionó ningún ID de recurso.")
    st.stop()

# Obtener el idioma seleccionado
idioma_seleccionado = st.session_state.get('idioma_seleccionado', 'es')

# Cargar los datos del recurso
recurso, traducciones = cargar_datos_recurso(idioma_seleccionado, resource_id)

# Título de la página
st.title(f"{recurso['resource_name']}")

# Columnas para el diseño
cols = st.columns([3, 2])

with cols[0]:
    mostrar_informacion_general(recurso, traducciones)
    mostrar_caracteristicas_recurso(recurso, traducciones)
    mostrar_accesibilidad_y_senalizacion(recurso, traducciones)
    mostrar_servicios_y_estado(recurso, traducciones)

with cols[1]:
    mostrar_imagenes(recurso)

# Botón para regresar a la página principal
if st.sidebar.button(traducciones.get('volver_al_mapa', 'Volver al Mapa')):
    st.session_state['resource_id'] = None
    st.switch_page("app.py")