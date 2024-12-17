import streamlit as st
from streamlit_folium import st_folium
from src.data_utils import filtrar_datos, cargar_datos, inicializar_estado, seleccionar_idioma, seleccionar_categorias, mostrar_logo, seleccionar_ruta
from src.draw_routes import convertir_coordenadas, procesar_rutas, cargar_dataset_rutas
from src.create_map import crear_mapa
import pandas as pd

# Configura la página para que use el diseño ancho
st.set_page_config(layout="wide", initial_sidebar_state="collapsed", menu_items=None)

def mostrar_mapa(datos_filtrados, traducciones, ruta_predefinida, rutas_df):
    mapa = crear_mapa(datos_filtrados, traducciones)
    if ruta_predefinida:
        recurso_ids = procesar_rutas(mapa, rutas_df, ruta_predefinida)
        if recurso_ids:
            #print('recursos_ids:', recurso_ids)
            recurso_ids = [int(rid) for rid in recurso_ids if rid.isdigit()]
            #print('Tipos de recurso_ids:', [type(rid) for rid in recurso_ids])
            #print("d_filtors:", datos_filtrados['id'].dtype)
            datos_filtrados['id'] = datos_filtrados['id'].astype(int)
            datos_filtrados_por_id = datos_filtrados[datos_filtrados['id'].isin(recurso_ids)]
            #print('datos_filtrados:', datos_filtrados_por_id)
            st.session_state['recurso_seleccionados_ids'] = datos_filtrados_por_id['id'].unique().tolist()
            print(f"Categorías seleccionadas: {st.session_state['recurso_seleccionados_ids']}")
    salida = st_folium(mapa, height=2000, use_container_width=True)
    return salida

def mostrar_detalles_recurso(salida, datos, traducciones):
    recurso = None
    if salida is not None and salida.get('last_object_clicked'):
        lat = salida['last_object_clicked']['lat']
        lng = salida['last_object_clicked']['lng']
        for _, fila in datos.iterrows():
            coords = convertir_coordenadas(fila['lat_long'])
            if coords and abs(coords[0] - lat) < 0.0001 and abs(coords[1] - lng) < 0.0001:
                recurso = fila
                break
        if recurso is not None:
            st.session_state['selected_resource_id'] = recurso['id']
            st.success(traducciones["resource_selected"].format(resource_name=recurso['resource_name']))
    return recurso

def mostrar_detalles_ruta(rutas_df, traducciones):
    ruta = None
    if 'selected_route_id' in st.session_state and st.session_state['selected_route_id'] is not None:
        ruta = rutas_df[rutas_df['id'] == st.session_state['selected_route_id']]
        if not ruta.empty:
            ruta = ruta.iloc[0]
            st.success(traducciones["route_selected"].format(route_name=ruta['route_name']))
        else:
            st.warning(traducciones["messages"]["route_not_found"])
    return ruta

def aplicar_css_personalizado(ruta_label, categorias_label):
    st.markdown(f"""
    <style>
        [data-testid="stImageContainer"] {{
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 99999999 !important;
            max-width: 130px;
            
        }}
            
        [data-testid="stSelectbox"]:has(input[aria-label$="{ruta_label}"]) {{
            position: fixed;
            top: 10px;
            right: 130px;
            z-index: 99999999 !important;
            width: auto !important;
            max-width: 130px;
            
        }}
        [data-testid="stSelectbox"]:has(input[aria-label$="Idioma:"]) {{
            position: fixed;
            bottom: 10px;
            left: 10px;
            z-index: 99999999 !important;
            width: auto !important;
        }}
        
        [data-testid="stSelectbox"]:has(input[aria-label$="Idioma:"]) label {{
            display: none;
        }}

        [data-testid="stMultiSelect"]{{
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 99999999 !important;
            width: auto !important;
            max-width: 110px;
        }}
        
        .stButton button {{
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
        }}

        .stButton button:after {{
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
        }}

        .stButton button:focus,
        .stButton button:hover {{
            background: #E65A3E;
            color: white !important;
        }}

        .stButton button:active:after {{
            width: 300px;
            height: 300px;
        }}

        /* Botón 1 */
        .element-container:has(#button-after-1) + div button {{
            position: fixed;
            bottom: 60px;
            right: 10px;
            z-index: 100000 !important;
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: #FC6E51;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease;
            width: auto;
            margin-bottom: 10px; /* Espacio inferior */
        }}

        .element-container:has(#button-after-1) + div button:hover {{
            background-color: #E65A3E;
        }}

        /* Botón 2 */
        .element-container:has(#button-after-2) + div button {{
            position: fixed;
            bottom: 10px; /* Ajusta la posición para evitar superposición */
            right: 10px;
            z-index: 100000 !important;
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: #FC6E51;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease;
            width: auto;
            margin-bottom: 10px; /* Espacio inferior */
        }}

        .element-container:has(#button-after-2) + div button:hover {{
            background-color: #E65A3E;
        }}

        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {{
            width: 0px;
        }}

        .eyeqlp53.st-emotion-cache-qsoh6x.ex0cdmw0 {{
            display: none;
        }}

        .st-emotion-cache-wfudur e1f1d6gn4 {{
            display: none;
        }}
            </style>
            """, unsafe_allow_html=True)

def aplicar_css_global():
    
    st.markdown(f"""
    <style>
        html, body{{
            height: 100%;
            width: 100%;
        }}
        #map-div {{
            height: 100vh;
            width: 100vh;
            margin: 0;
        }}
        .stAppHeader {{
            display: none;
        }}
        .stAppToolbar {{
            display: none;
        }}
        .stMainBlockContainer {{
            padding: 0 !important;
            margin: 0 !important;
            overflow: hidden;
        }}
        .stCheckbox > label{{
            margin-bottom: 0.1rem;
        }}
        .footer {{
            display: none;
        }}
    </style>
    """, unsafe_allow_html=True)

def main():
    inicializar_estado()
    
    # Cargar configuración inicial desde session_state o usar valores por defecto
    if 'idioma_seleccionado' not in st.session_state:
        st.session_state['idioma_seleccionado'] = 'pt'

    # Cargar datos según el idioma en session_state
    datos, traducciones = cargar_datos(st.session_state['idioma_seleccionado'])
    if datos.empty:
        st.error("No hay datos disponibles.")
        return
    
    category_mapping_ruta = traducciones.get("category_mapping_ruta", {})
    rutas_df = cargar_dataset_rutas(st.session_state['idioma_seleccionado'], category_mapping_ruta)
    
    if 'categorias_seleccionadas_ids' not in st.session_state:
        st.session_state['categorias_seleccionadas_ids'] = []
        
    if 'recurso_seleccionados_ids' not in st.session_state:
        st.session_state['recurso_seleccionados_ids'] = []
        
    # Determinar ruta seleccionada, o None por defecto
    if 'selected_route_name' not in st.session_state:
        st.session_state['selected_route_name'] = None

    # Filtrar datos según categorías en session_state
    datos_filtrados = filtrar_datos(
        datos,
        st.session_state['categorias_seleccionadas_ids'],
        st.session_state.get('recurso_seleccionados_ids', None)
    )

    # Ruta predefinida desde session_state
    ruta_predefinida = st.session_state['selected_route_name']
    
    print('categorias_seleccionadas_ids1:', st.session_state['categorias_seleccionadas_ids'])

    # Renderizar el mapa UNA SOLA VEZ en cada ejecución, con los datos actuales
    salida = mostrar_mapa(datos_filtrados, traducciones, st.session_state['selected_route_name'], rutas_df)

    print('categorias_seleccionadasde_numero:', st.session_state['recurso_seleccionados_ids'])
    print('categorias_seleccionadas_ids2:', st.session_state['categorias_seleccionadas_ids'])
    
    idioma_seleccionado = seleccionar_idioma()
    st.session_state['idioma_seleccionado'] = idioma_seleccionado

    categorias_seleccionadas_ids = seleccionar_categorias(traducciones, datos)
    st.session_state['categorias_seleccionadas_ids'] = categorias_seleccionadas_ids
    
    seleccionar_ruta(traducciones)
    
    ruta_label = traducciones.get("select_route", "Seleccionar ruta")
    categorias_label = traducciones.get("select_category", "Categorias:")
    
    if datos.empty:
        st.error(traducciones["messages"]["no_data_error"])
        return
    
    aplicar_css_personalizado(ruta_label, categorias_label)
    mostrar_detalles_recurso(salida, datos, traducciones)
    mostrar_detalles_ruta(rutas_df, traducciones)
    
    
    st.markdown('<span id="button-after-1"></span>', unsafe_allow_html=True)
    
    # Agregar el Botón Fijo en la Esquina Superior Izquierda
    if st.button(traducciones["buttons"]["details_resource_button"]):
        if st.session_state['selected_resource_id'] is not None:
            st.session_state['resource_id'] = st.session_state['selected_resource_id']
            st.switch_page("pages/detalle_recurso.py")
        else:
            st.warning(traducciones["messages"]["select_resource_warning"])
    
    st.markdown('<span id="button-after-2"></span>', unsafe_allow_html=True)
    
    if st.button(traducciones["buttons"]["details_route_button"], key='details_route_button'):
        if st.session_state['selected_route_id'] is not None:
            st.session_state['route_id'] = st.session_state['selected_route_id']
            st.switch_page("pages/detalle_ruta.py")
        else:
            st.warning(traducciones["messages"]["select_route_warning"])

    aplicar_css_global()
    mostrar_logo()
    
if __name__ == "__main__":
    main()