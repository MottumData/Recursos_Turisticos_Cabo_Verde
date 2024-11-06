import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import folium
from folium import plugins
from streamlit_folium import st_folium

# Configura la página para que use el diseño ancho
st.set_page_config(layout="wide")

# Establece el título de la aplicación
st.title('Mapa Interactivo con Datos de Excel')

# Carga los datos desde el archivo CSV
ruta_archivo = 'data/santiago_cabo_verde_localizaciones.csv'
datos = pd.read_csv(ruta_archivo)

# Añade un widget de selección para filtrar por nombre
st.sidebar.title("Filtros")
nombres = datos['nombre'].unique()
nombre_seleccionado = st.selectbox('Selecciona un nombre para filtrar', nombres)

# Filtra los datos según la selección
datos_filtrados = datos[datos['nombre'] == nombre_seleccionado]

# Crea el mapa utilizando Folium
mapa = folium.Map(
    location=[datos_filtrados['Latitud'].mean(), datos_filtrados['Longitud'].mean()],
    zoom_start=10
)

plugins.Fullscreen(                                                         
        position = "topright",                                   
        title = "Open full-screen map",                       
        title_cancel = "Close full-screen map",                      
        force_separate_button = True,                                         
    ).add_to(mapa) 

# Añade marcadores al mapa
for _, fila in datos_filtrados.iterrows():
    folium.Marker(
        location=[fila['Latitud'], fila['Longitud']],
        popup=fila['nombre']
    ).add_to(mapa)

st.markdown(
    """
    <style>
    .main .block-container {
        padding: 0;
    }
    .main .block-container .element-container {
        padding: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st_folium(mapa, width="100%", height=600)

# Muestra los datos cargados
st.write('Datos cargados:')
st.dataframe(datos)

st.write('Datos filtrados:')