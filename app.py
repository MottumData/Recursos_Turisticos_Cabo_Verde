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

def filtrar_datos(datos, categorias_seleccionadas):
    if categorias_seleccionadas:
        datos = datos[datos['category_id'].isin(categorias_seleccionadas)]
    return datos

def crear_mapa(datos, traducciones):

    mapa = folium.Map(
        location=[15.1111, -23.6167],
        zoom_start=10,
        tiles=None
    )
    
    folium.TileLayer('OpenStreetMap', name='OpenStreetMap', show=True).add_to(mapa)
    folium.TileLayer('OpenTopoMap', name='OpenTopoMap', show=False).add_to(mapa)
    #folium.TileLayer('Stamen Watercolor', name='Stamen Watercolor', show=False).add_to(mapa)
    #folium.TileLayer('Stamen Terrain', name='Stamen Terrain', show=False).add_to(mapa)
    #folium.TileLayer('Stamen Toner', name='Stamen Toner', show=False).add_to(mapa)
    folium.TileLayer('CartoDB positron', name='CartoDB Positron', show=False).add_to(mapa)
    folium.TileLayer('CartoDB dark_matter', name='CartoDB Dark Matter', show=False).add_to(mapa)

    # Agregar control de capas
    folium.LayerControl().add_to(mapa)

    plugins.Fullscreen(
        position="topright",
        title=traducciones.get("abrir_pantalla_completa", "Open full-screen map"),
        title_cancel=traducciones.get("cerrar_pantalla_completa", "Close full-screen map"),
        force_separate_button=True,
    ).add_to(mapa)
    
    category_icons = {
    'category_natural_places': {'color': 'lightgreen', 'icon': 'tree'},
    'category_beaches_coastal': {'color': 'darkgreen', 'icon': 'umbrella-beach'},
    'category_mountains': {'color': 'green', 'icon': 'mountain'},
    'category_flora_fauna': {'color': 'lightgreen', 'icon': 'binoculars'},
    'category_vales': {'color': 'green', 'icon': 'tree'},
    'category_architectural_heritage': {'color': 'blue', 'icon': 'university'},
    'category_museums': {'color': 'darkblue', 'icon': 'university'},
    'category_representative_works': {'color': 'lightblue', 'icon': 'palette'},
    'category_ethnography_folklore': {'color': 'orange', 'icon': 'users'},
    'category_spiritual_folklore': {'color': 'orange', 'icon': 'church'},
    'category_ethnic_groups': {'color': 'orange', 'icon': 'users'},
    'category_scientific_achievements': {'color': 'purple', 'icon': 'flask'},
    'category_engineering_works': {'color': 'purple', 'icon': 'cogs'},
    'category_human_settlements': {'color': 'brown', 'icon': 'home'},
    'category_geological_formations': {'color': 'darkpurple', 'icon': 'gem'},
    'category_archaeological_legacy': {'color': 'maroon', 'icon': 'landmark'},
    'category_farms': {'color': 'olive', 'icon': 'tractor'},
    'category_others': {'color': 'gray', 'icon': 'question-circle'},
    }

    for index, fila in datos.iterrows():
        coordenadas = convertir_coordenadas(fila['lat_long'])
        if coordenadas:
            lat, lon = coordenadas
            nombre_recurso = fila['resource_name']
            categoria = fila['category_id']
            resource_id = fila['id']
            icono = category_icons.get(categoria, {'color': 'gray', 'icon': 'question-circle'})
            
            # Incluir resource_id en el popup de manera estructurada
            mas_informacion = traducciones.get("more_information", "Más información")
            
            popup_html = f'''
            <b>{nombre_recurso}</b><br>
            <a href="#" onclick="parent.scrollToBottom(); return false;">{mas_informacion}</a>
            '''

            # Agregar el marcador al mapa con el popup modificado
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
    
    idioma_seleccionado = st.sidebar.selectbox(
            "Idioma:",
            idiomas_disponibles
    )

    # Cargar las traducciones para el idioma seleccionado
    traducciones = cargar_traducciones(idioma_seleccionado)
    
    category_mapping = traducciones.get("category_mapping", {})
    
    # Cargar el dataset correspondiente y aplicar el mapeo de columnas
    datos = cargar_dataset(idioma_seleccionado, category_mapping)

    if datos.empty:
        st.error("No hay datos disponibles para este idioma.")
        return

    # Obtener todas las categorías disponibles con sus identificadores
    categorias = datos[['category_id', 'category']].drop_duplicates().sort_values('category')

    # Crear un diccionario para mapear etiquetas a identificadores
    categoria_dict = dict(zip(categorias['category'], categorias['category_id']))

    # Obtener las etiquetas traducidas para mostrar al usuario
    categorias_labels = list(categoria_dict.keys())

    # Crear el multiselect usando las etiquetas traducidas
    categorias_seleccionadas_labels = st.sidebar.multiselect(
        traducciones.get("select_category", "Categorias:"),
        categorias_labels
    )

    # Mapear las etiquetas seleccionadas a los identificadores
    categorias_seleccionadas_ids = [categoria_dict[label] for label in categorias_seleccionadas_labels]
    
    datos_filtrados = filtrar_datos(datos, categorias_seleccionadas_ids)

    # Nuevo: Cargar las rutas y definir el selector de rutas fuera de la función
    rutas_df = cargar_rutas()
    ruta_predefinida = None
    if not rutas_df.empty:
        ruta_predefinida = st.sidebar.selectbox(
            traducciones.get("select_route", "Seleccionar ruta"),
            ['Ninguna'] + list(rutas_df['Nombre de la ruta'].unique())
        )
        if ruta_predefinida == 'Ninguna':
            ruta_predefinida = None

    # Crear el mapa utilizando Folium centrado en Cabo Verde
    
    mapa = crear_mapa(datos_filtrados, traducciones)
    
    if ruta_predefinida:
        procesar_rutas(mapa, rutas_df, ruta_predefinida)
        
    # Mostrar el mapa
    salida = st_folium(mapa, height=700, use_container_width=True,)
    
    # --- Código Añadido: Detectar resource_id y Redirigir ---
    resource_id_clicked = st.session_state.get('resource_id', None)
    
    if resource_id_clicked:
        st.session_state.pop('resource_id', None)
        st.query_params(resource_id=resource_id_clicked)
        st.switch_page("Detalle del Recurso")
        return
    
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
    # Inyectar la función JavaScript para hacer scroll al fondo
    st.markdown("""
        <script>
        #bottom {
            height: 50px;
        }
        function scrollToBottom() {
            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        }
        </script>
    """, unsafe_allow_html=True)
                          
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
            /* Ajustar el contenedor principal para usar Flexbox */
            .stMainBlockContainer {{
                padding: 0 !important;
                margin: 0 !important;
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