import streamlit as st
from streamlit_folium import st_folium
from src.data_utils import filtrar_datos, cargar_datos, inicializar_estado, seleccionar_idioma, seleccionar_categorias, seleccionar_ruta, mostrar_logo
from src.draw_routes import convertir_coordenadas, procesar_rutas
from src.create_map import crear_mapa
import pandas as pd

# Configura la página para que use el diseño ancho
st.set_page_config(layout="wide")

def mostrar_mapa(datos_filtrados, traducciones, ruta_predefinida, rutas_df):
    mapa = crear_mapa(datos_filtrados, traducciones)
    if ruta_predefinida:
        procesar_rutas(mapa, rutas_df, ruta_predefinida)
    salida = st_folium(mapa, height=2000, use_container_width=True)
    return salida

def mostrar_detalles_recurso(salida, datos):
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
            st.sidebar.success(f"Recurso seleccionado: {recurso['resource_name']}")
        else:
            st.sidebar.warning("No se encontró un recurso en la ubicación clickeada.")
    return recurso

def mostrar_detalles_ruta(rutas_df):
    ruta = None
    if 'selected_route_id' in st.session_state and st.session_state['selected_route_id'] is not None:
        ruta = rutas_df[rutas_df['Nombre de la ruta'] == st.session_state['selected_route_id']]
        if not ruta.empty:
            ruta = ruta.iloc[0]
            st.sidebar.success(f"Ruta seleccionada: {ruta['Nombre de la ruta']}")
        else:
            st.sidebar.warning("No se encontró la ruta seleccionada.")
    return ruta

def aplicar_css_personalizado():
    st.markdown("""
    <style>
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

def aplicar_css_global():
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
    </style>
    """, unsafe_allow_html=True)
    
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
    mostrar_logo()
    idioma_seleccionado = seleccionar_idioma()
    datos, traducciones = cargar_datos(idioma_seleccionado)
    
    if datos.empty:
        st.error("No hay datos disponibles para este idioma.")
        return

    categorias_seleccionadas_ids = seleccionar_categorias(traducciones, datos)
    datos_filtrados = filtrar_datos(datos, categorias_seleccionadas_ids)
    ruta_predefinida, rutas_df = seleccionar_ruta(traducciones)
    salida = mostrar_mapa(datos_filtrados, traducciones, ruta_predefinida, rutas_df)
    
    aplicar_css_personalizado()
    
    if st.sidebar.button('Detalles de Recurso'):
        if st.session_state['selected_resource_id'] is not None:
            st.session_state['resource_id'] = st.session_state['selected_resource_id']
            st.switch_page("pages/detalle_recurso.py")
        else:
            st.sidebar.warning("Por favor, selecciona un recurso en el mapa antes de ver más información.")
    mostrar_detalles_recurso(salida, datos)

    mostrar_detalles_ruta(rutas_df)

    aplicar_css_global()
    
    if st.sidebar.button('Detalle de ruta'):
        if st.session_state['selected_route_id'] is not None:
            st.session_state['route_id'] = st.session_state['selected_route_id']
            st.switch_page("pages/detalle_ruta.py")
        else:
            st.sidebar.warning("Por favor, selecciona una ruta en el mapa antes de ver más información.")

if __name__ == "__main__":
    main()