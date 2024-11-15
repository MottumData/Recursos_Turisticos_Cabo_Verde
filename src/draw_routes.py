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

def dibujar_ruta(mapa, inicio_coords, fin_coords, G, nombre_ruta):
    try:
        # osmnx.nearest_nodes espera (lon, lat)
        nodo_inicio = ox.nearest_nodes(G, inicio_coords[1], inicio_coords[0])
        nodo_fin = ox.nearest_nodes(G, fin_coords[1], fin_coords[0])
    except Exception as e:
        st.error(f"No se pudo encontrar nodos cercanos para {nombre_ruta}: {e}")
        return
    
    try:
        ruta = nx.shortest_path(G, nodo_inicio, nodo_fin, weight='length')
    except nx.NetworkXNoPath:
        st.error(f"No se encontró una ruta entre los puntos seleccionados para {nombre_ruta}.")
        return
    
    ruta_coords = [(G.nodes[nodo]['y'], G.nodes[nodo]['x']) for nodo in ruta]  # (lat, lon)
    
    # Dibujar la ruta en el mapa
    folium.PolyLine(
        ruta_coords,
        color='blue',
        weight=4,
        opacity=0.7,
        tooltip=nombre_ruta
    ).add_to(mapa)
    
    # Opcional: Añadir marcadores de inicio y fin solo en el primer y último segmento
    if 'Segmento Inicial' in nombre_ruta:
        folium.Marker(
            location=inicio_coords,
            popup=f"Inicio: {nombre_ruta}",
            icon=folium.Icon(color='green', icon='play')
        ).add_to(mapa)
    if 'Segmento Final' in nombre_ruta:
        folium.Marker(
            location=fin_coords,
            popup=f"Fin: {nombre_ruta}",
            icon=folium.Icon(color='red', icon='stop')
        ).add_to(mapa)
        
@st.cache_data
def cargar_rutas():
    ruta = "data/rutas_cabo_verde.csv"
    if os.path.exists(ruta):
        df = pd.read_csv(ruta)
        return df
    else:
        st.error("El archivo rutas_cabo_verde.csv no existe.")
        return pd.DataFrame()