import streamlit as st
import pandas as pd
import folium
from folium import plugins
from streamlit_folium import st_folium
import json
import os
import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim
from shapely.geometry import Point
from shapely.ops import unary_union
import geopandas as gpd
import streamlit.components.v1 as components

# Importar funciones desde los nuevos módulos
from src.data_utils import cargar_dataset, cargar_traducciones, obtener_idiomas
from src.draw_routes import convertir_coordenadas, obtener_coordenadas, cargar_red_carreteras_por_puntos, dibujar_ruta, cargar_rutas

# Configura la página para que use el diseño ancho
st.set_page_config(layout="wide")

capas = {
        'OpenStreetMap': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        'Stamen Terrain': 'https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg',
        'Stamen Toner': 'http://tile.stamen.com/toner/{z}/{x}/{y}.png',
        'CartoDB positron': 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
        'CartoDB dark_matter': 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
    }

atribuciones = {
    'OpenStreetMap': '&copy; OpenStreetMap contributors',
    'Stamen Terrain': 'Map tiles by Stamen Design, CC BY 3.0',
    'Stamen Toner': 'Map tiles by Stamen Design, CC BY 3.0',
    'CartoDB positron': '&copy; OpenStreetMap contributors & CARTO',
    'CartoDB dark_matter': '&copy; OpenStreetMap contributors & CARTO'
}

def filtrar_datos(datos, ilha_seleccionada, categorias_seleccionadas):
    if ilha_seleccionada != 'Todos':
        datos = datos[datos['island'] == ilha_seleccionada]
    if categorias_seleccionadas:
        datos = datos[datos['category'].isin(categorias_seleccionadas)]
    return datos

def crear_mapa(datos, capa_seleccionada, traducciones):

    mapa = folium.Map(
        location=[15.1111, -23.6167],
        zoom_start=10,
        tiles=capas[capa_seleccionada],
        attr=atribuciones[capa_seleccionada]
    )

    plugins.Fullscreen(
        position="topright",
        title=traducciones.get("abrir_pantalla_completa", "Open full-screen map"),
        title_cancel=traducciones.get("cerrar_pantalla_completa", "Close full-screen map"),
        force_separate_button=True,
    ).add_to(mapa)
    
    category_icons = {
    'Natural Places': {'color': 'lightgreen', 'icon': 'tree'},
    'Beaches and Coastal Locations': {'color': 'darkgreen', 'icon': 'umbrella-beach'},
    'Mountains and Mountains': {'color': 'green', 'icon': 'mountain'},
    'Flora and Fauna Observation Sites': {'color': 'lightgreen', 'icon': 'binoculars'},
    'Vales': {'color': 'green', 'icon': 'tree'},
    
    'Architectural and Artistic Heritage': {'color': 'blue', 'icon': 'university'},
    'Museums and Exhibition Halls': {'color': 'darkblue', 'icon': 'university'},
    'Representative Works of Art': {'color': 'lightblue', 'icon': 'palette'},
    
    'Ethnography and folklore': {'color': 'orange', 'icon': 'users'},
    'Spiritual Folklore': {'color': 'orange', 'icon': 'church'},
    'Ethnic Groups': {'color': 'orange', 'icon': 'users'},
    
    'Scientific Technical Achievements': {'color': 'purple', 'icon': 'flask'},
    'Engineering Works': {'color': 'purple', 'icon': 'cogs'},
    
    'Human Settlements and Living Architecture': {'color': 'brown', 'icon': 'home'},
    
    'Geological and Paleontological Formations': {'color': 'darkpurple', 'icon': 'gem'},
    'Archaeological Legacy': {'color': 'maroon', 'icon': 'landmark'},
    
    'Farms': {'color': 'olive', 'icon': 'tractor'},
    
    'Others': {'color': 'gray', 'icon': 'question-circle'},
}

    for index, fila in datos.iterrows():
        coordenadas = convertir_coordenadas(fila['lat_long'])
        if coordenadas:
            lat, lon = coordenadas
            nombre_recurso = fila['resource_name']
            categoria = fila['category']
            resource_id = fila['id']
            icono = category_icons.get(categoria, {'color': 'gray', 'icon': 'question-circle'})
            popup_html = f"""
            <b>{nombre_recurso}</b><br>
            <a href="?resource_id={resource_id}" target="_self">
                <button style="background-color:#4CAF50;color:white;padding:5px 10px;border:none;border-radius:3px;cursor:pointer;">
                    Ver Detalles
                </button>
            </a>
            """

            # Agregar el marcador al mapa
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=nombre_recurso,
                icon=folium.Icon(color=icono['color'], icon=icono['icon'], prefix='fa')
            ).add_to(mapa)
    return mapa

def procesar_rutas(mapa, rutas_df, ruta_predefinida):
    if ruta_predefinida:
        ruta = rutas_df[rutas_df['Nombre de la ruta'] == ruta_predefinida].iloc[0]
        recursos_georeferenciados = ruta['Recursos Georeferenciados']
        
        # Parsear las coordenadas
        puntos = recursos_georeferenciados.split(';')
        coords = []
        municipios = ruta['Municipios por los que transcurre'].split(',')
        for punto in puntos:
            try:
                parte = punto.strip().split(':')[1].strip().strip('[]')
                lat, lon = map(float, parte.split(','))
                coords.append((lat, lon))
            except (IndexError, ValueError):
                st.error(f"Formato inválido en Recursos Georeferenciados para la ruta {ruta_predefinida}.")
                coords = []
                break
        
        if len(coords) >= 2:
            nombre_ruta = ruta_predefinida
            
            # Cargar la red de carreteras alrededor de los puntos de la ruta
            with st.spinner('Cargando la red de carreteras para la ruta seleccionada...'):
                G = cargar_red_carreteras_por_puntos(coords)
            
            for i in range(len(coords) - 1):
                inicio_coords = coords[i]
                fin_coords = coords[i + 1]
                if i == 0:
                    segmento_nombre = f"{nombre_ruta} Segmento Inicial"
                elif i == len(coords) - 2:
                    segmento_nombre = f"{nombre_ruta} Segmento Final"
                else:
                    segmento_nombre = f"{nombre_ruta} Segmento {i+1}"
                dibujar_ruta(mapa, inicio_coords, fin_coords, G, segmento_nombre)
        else:
            st.error(f"No hay suficientes puntos para dibujar la ruta {ruta_predefinida}.")



def main(): # Recarga una vez después de 5 segu
    st.sidebar.image('assets/Logo_cabo_verde.png')
    
    # Obtener los parámetros de la URL
    query_params = st.query_params
    resource_id = query_params.get("resource_id", [None])[0]

    if resource_id is not None:
        # Guardar el resource_id en session_state y redirigir
        st.session_state['resource_id'] = resource_id
        st.query_params # Limpiar los parámetros de la URL
        st.switch_page("Detalle del Recurso")
        return
    
    
    idiomas_disponibles = obtener_idiomas()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="custom-selectbox">', unsafe_allow_html=True)
        idioma_seleccionado = st.selectbox(
            "Seleccione su idioma",
            idiomas_disponibles
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Cargar las traducciones para el idioma seleccionado
    traducciones = cargar_traducciones(idioma_seleccionado)
    
    # Cargar el dataset correspondiente y aplicar el mapeo de columnas
    datos = cargar_dataset(idioma_seleccionado)

    if datos.empty:
        st.error("No hay datos disponibles para este idioma.")
        return
    
    with col2:
        st.markdown('<div class="custom-selectbox">', unsafe_allow_html=True)
        capa_seleccionada = st.selectbox(
            "Seleccione la capa",
            list(capas.keys())
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Filtrar por isla
    ilha_seleccionada = st.sidebar.selectbox(
        traducciones.get("seleccionar_ilha", "Seleccionar isla"),
        ['Todos'] + sorted(datos['island'].dropna().unique())
    )

    # Filtrar por categoría
    categorias = sorted(datos['category'].dropna().unique())
    categorias_seleccionadas = st.sidebar.multiselect(
        traducciones.get("seleccionar_categorias", "Seleccionar categorías"),
        categorias
    )

    # Nuevo: Cargar las rutas y definir el selector de rutas fuera de la función
    rutas_df = cargar_rutas()
    ruta_predefinida = None
    if not rutas_df.empty:
        st.sidebar.subheader("Rutas Predefinidas")
        ruta_predefinida = st.sidebar.selectbox(
            "Seleccione una ruta predefinida",
            ['Ninguna'] + list(rutas_df['Nombre de la ruta'].unique())
        )
        if ruta_predefinida == 'Ninguna':
            ruta_predefinida = None

    # Filtrar los datos según las selecciones
    datos_filtrados = filtrar_datos(datos, ilha_seleccionada, categorias_seleccionadas)

    # Crear el mapa utilizando Folium centrado en Cabo Verde
    
    mapa = crear_mapa(datos_filtrados, capa_seleccionada, traducciones)
    
    if ruta_predefinida:
        procesar_rutas(mapa, rutas_df, ruta_predefinida)
        
    # Mostrar el mapa
    salida = st_folium(mapa, width="Full")
    
    recurso = None
            
    if salida is not None and salida.get('last_object_clicked'):
        lat = salida['last_object_clicked']['lat']
        lng = salida['last_object_clicked']['lng']
        
        # Encontrar el recurso más cercano a las coordenadas clickeadas
        recurso = None
        for _, fila in datos.iterrows():
            coords = convertir_coordenadas(fila['lat_long'])
            if coords and abs(coords[0] - lat) < 0.0001 and abs(coords[1] - lng) < 0.0001:
                recurso = fila
                break
    if recurso is not None:
        # Crear un contenedor para el panel de detalles
        with st.container():
            with st.expander(traducciones.get("detalles_recurso", "Detalles del Recurso"), expanded=True):
                cols = st.columns([3, 2])
                
                with cols[0]:
                    st.markdown(f"### {recurso['resource_name']}")
                    
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
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <style>
            .stAppHeader {{
                display: none;
            }}
            .stAppToolbar {{
                display: none;
            }}
            /* Ajustar el contenedor principal para usar Flexbox */
            .stMainBlockContainer {{
                padding: 0 !important;
            }}
            .stCheckbox > label{{
                margin-bottom: 0.1rem;
            }}
            .footer {{
                display: none;
            }}
        </style>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()