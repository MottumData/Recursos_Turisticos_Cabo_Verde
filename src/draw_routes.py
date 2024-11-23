# draw_routes.py

import streamlit as st
import folium
import osmnx as ox
import networkx as nx
from shapely.geometry import Point
import geopandas as gpd
import pandas as pd
from geopy.geocoders import Nominatim
import os

def convertir_coordenadas(coordenadas):
    try:
        lat, lon = map(float, coordenadas.split(','))
        return lat, lon
    except ValueError:
        return None

@st.cache_data
def obtener_coordenadas(lugar):
    geolocator = Nominatim(user_agent="mi_aplicacion")
    location = geolocator.geocode(lugar)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

@st.cache_resource
def cargar_red_carreteras_por_puntos(coords):
    margin = 0.02
    lats, lons = zip(*coords)
    north, south = max(lats) + margin, min(lats) - margin
    east, west = max(lons) + margin, min(lons) - margin
    G = ox.graph_from_bbox(north, south, east, west, network_type='drive')
    return G


def dibujar_ruta(mapa, coords, G, nombre_ruta):
    try:
        # Convertir las coordenadas a nodos en la red de carreteras
        nodos = [ox.nearest_nodes(G, coord[1], coord[0]) for coord in coords]
    except Exception as e:
        st.error(f"No se pudo encontrar nodos cercanos para {nombre_ruta}: {e}")
        return
    
    ruta_coords = []
    for i in range(len(nodos) - 1):
        try:
            ruta_segmento = nx.shortest_path(G, nodos[i], nodos[i + 1], weight='length')
            ruta_coords.extend([(G.nodes[nodo]['y'], G.nodes[nodo]['x']) for nodo in ruta_segmento])
        except nx.NetworkXNoPath:
            st.error(f"No se encontró una ruta entre los puntos seleccionados para {nombre_ruta}.")
            return
    
    highlight = {
        'color': 'yellow',
        'weight': 6,
        'opacity': 1.0
    }
    # Dibujar la ruta en el mapa
    folium.PolyLine(
        ruta_coords,
        color='blue',
        weight=4,
        opacity=0.7,
        popup=nombre_ruta,
        tooltip=None,
        interactive=False,  # Deshabilitar la interacción
        highlight_function=lambda x: highlight
    ).add_to(mapa)
    
    # Añadir marcadores de inicio y fin
    folium.Marker(
        location=coords[0],
        popup=f"Inicio: {nombre_ruta}",
        icon=folium.Icon(color='green', icon='play')
    ).add_to(mapa)
    folium.Marker(
        location=coords[-1],
        popup=f"Fin: {nombre_ruta}",
        icon=folium.Icon(color='red', icon='stop')
    ).add_to(mapa)
        
    
def cargar_dataset_rutas(idioma_seleccionado):
    # Aquí debes cargar el dataset específico de las rutas
    # Por ejemplo, podrías cargar un archivo CSV o una base de datos
    # Asegúrate de que el dataset esté filtrado por el idioma seleccionado
    archivo_rutas = f"data/rutas_cabo_verde_{idioma_seleccionado}.csv"
    datos = pd.read_csv(archivo_rutas)
    return datos
    
def procesar_rutas(mapa, rutas_df, ruta_predefinida):
    if ruta_predefinida:
        ruta = rutas_df[rutas_df['Nombre de la ruta'] == ruta_predefinida]
        if not ruta.empty:
            ruta = ruta.iloc[0]
            recursos_georeferenciados = ruta['Recursos Georeferenciados']
            puntos = recursos_georeferenciados.split(';')
            coords = []
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
                
                # Dibujar la ruta completa como un solo segmento
                dibujar_ruta(mapa, coords, G, nombre_ruta)
            else:
                st.error(f"No hay suficientes puntos para dibujar la ruta {ruta_predefinida}.")