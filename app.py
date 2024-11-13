import streamlit as st
import pandas as pd
import folium
from folium import plugins
from streamlit_folium import st_folium
import json
import os

# Configura la página para que use el diseño ancho
st.set_page_config(layout="wide")

# Mapeo de nombres de columnas por idioma
column_mappings = {
    'es': {  # Español
        'Lat-Long': 'lat_long',
        'Nombre del recurso turístico': 'resource_name',
        'isla': 'island',
        'Consejo': 'council',
        'Parroquia': 'parish',
        'Aldea': 'village',
        'Vecindario': 'neighborhood',
        'Clasificación': 'classification',
        'Cara': 'category',
        'Descripción del Producto': 'description',
        'Elementos materiales asociados': 'material_elements',
        'Elementos naturales asociados': 'natural_elements',
        'Acceso a recursos [dominio público o privado]': 'resource_access',
        'Imágenes destacadas': 'feature_images',
        'Imágenes de la característica 1': 'feature_image_1',
        'Datos pendientes de interés turístico': 'pending_tourist_data',
        'Singularidad que lo diferencia de otros en la región': 'uniqueness',
        'Satisfacción del cliente con la función.': 'customer_satisfaction',
        'Posibilidades de exploración futura': 'future_exploration',
        'Intervenciones necesarias para su uso': 'required_interventions',
        'Acceso a recursos (tierra)': 'land_access',
        'Medios de viaje': 'travel_means',
        'Señalización (Dentro del municipio)': 'signage_within_municipality',
        'Señalización (Fuera del municipio)': 'signage_outside_municipality',
        'Señalización (Cerca)': 'signage_nearby',
        'Tipo de renda': 'income_type',
        'Aplica (Dentro del Recurso Turístico)': 'applies_within_resource',
        'Aplica (Fuera del Recurso Turístico)': 'applies_outside_resource',
        'IDENTIFICACIÓN': 'id',
        'Estado de conservación': 'conservation_status',
        'Otros Servicios Turísticos (Fuera del Complejo Turístico más cercano)': 'other_services_outside',
        'Servicios Básicos (Fuera del centro turístico más cercano)': 'basic_services_outside',
        'Servicios de emergencia (Fuera del complejo turístico más cercano)': 'emergency_services_outside',
        'Otros Servicios Turísticos (Dentro del Recurso Turístico)': 'other_services_within',
        'Servicios básicos (Dentro del Complejo Turístico)': 'basic_services_within',
        'Imágenes de la característica 2': 'feature_image_2',
        'Característica 3 imágenes': 'feature_image_3',
        'Característica 4 imágenes': 'feature_image_4',
        'Servicios de emergencia (Dentro del Complejo Turístico)': 'emergency_services_within',
        'Acceso al recurso (Marítimo)': 'maritime_access',
        'Nivel actual de uso': 'current_usage_level',
        'Acceso a recursos (aerotransportado)': 'air_access',
        'Medios de viaje 2': 'travel_means_2'
    },
    'en': {  # Inglés
        'Lat-Long': 'lat_long',
        'Tourist resource name': 'resource_name',
        'island': 'island',
        'Council': 'council',
        'Parish': 'parish',
        'Vila': 'village',
        'Neighborhood': 'neighborhood',
        'Classification': 'classification',
        'Cara': 'category',
        'Product Description': 'description',
        'Associated material elements': 'material_elements',
        'Associated natural elements': 'natural_elements',
        'Resource Access [Public or private domain]': 'resource_access',
        'Feature Images': 'feature_images',
        'Feature 1 Images': 'feature_image_1',
        'Pending data of tourist interest': 'pending_tourist_data',
        'Uniqueness that sets it apart from others in the region': 'uniqueness',
        'Customer satisfaction with the feature': 'customer_satisfaction',
        'Possibilities for future exploration': 'future_exploration',
        'Interventions required for its use': 'required_interventions',
        'Resource access (Land)': 'land_access',
        'Means of travel': 'travel_means',
        'Signage (Within the municipality)': 'signage_within_municipality',
        'Signage (Outside the municipality)': 'signage_outside_municipality',
        'Signage (Nearby)': 'signage_nearby',
        'Type of income': 'income_type',
        'Applies (Within the Tourist Resource)': 'applies_within_resource',
        'Applies (Outside the Tourist Resort)': 'applies_outside_resource',
        'ID': 'id',
        'Conservation status': 'conservation_status',
        'Other Tourist Services (Outside the nearest Tourist Resort)': 'other_services_outside',
        'Basic Services (Outside the nearest tourist resort)': 'basic_services_outside',
        'Emergency services (Outside the nearest tourist resort)': 'emergency_services_outside',
        'Other Tourist Services (Within the Tourist Resource)': 'other_services_within',
        'Basic services (Within the Tourist Resort)': 'basic_services_within',
        'Feature 2 Images': 'feature_image_2',
        'Feature 3 Images': 'feature_image_3',
        'Feature 4 Images': 'feature_image_4',
        'Emergency services (Within the Tourist Resort)': 'emergency_services_within',
        'Access to the resource (Maritime)': 'maritime_access',
        'Current level of usage': 'current_usage_level',
        'Resource Access (Airborne)': 'air_access',
        'Means of travel 2': 'travel_means_2'
    },
    'pt': {  # Portugués
        'Lat-Long': 'lat_long',
        'Nome do recurso turístico': 'resource_name',
        'ilha': 'island',
        'Conselho': 'council',
        'Freguesia': 'parish',
        'Vila': 'village',
        'Bairro': 'neighborhood',
        'Classificação': 'classification',
        'Cara': 'category',
        'Descrição do produto': 'description',
        'Elementos materiais associados': 'material_elements',
        'Elementos naturais associados': 'natural_elements',
        'Acesso ao Recurso [Domínio público ou privado]': 'resource_access',
        'Imagens do recurso': 'feature_images',
        'Imagens do recurso 1': 'feature_image_1',
        'Dados pendentes de interesse turístico': 'pending_tourist_data',
        'Singularidade que o diferencia dos demais da região': 'uniqueness',
        'Satisfação do cliente com o recurso': 'customer_satisfaction',
        'Possibilidades de exploração futura': 'future_exploration',
        'Intervenções necessárias para seu uso': 'required_interventions',
        'Acesso ao recurso (Terra)': 'land_access',
        'Meio de viagem': 'travel_means',
        'Sinalização (Dentro do município)': 'signage_within_municipality',
        'Sinalização (Fora do município)': 'signage_outside_municipality',
        'Sinalização (Na proximidade)': 'signage_nearby',
        'Tipo de renda': 'income_type',
        'Aplica (Dentro do Recurso Turístico)': 'applies_within_resource',
        'Aplica (Fora do Recurso Turístico)': 'applies_outside_resource',
        'ID': 'id',
        'Estado de conservação': 'conservation_status',
        'Outros Serviços Turísticos (Fora do Empreendimento Turístico da localidade mais próxima)': 'other_services_outside',
        'Serviços Básicos ( Fora do Empreendimento Turístico da localidade mais próxima)': 'basic_services_outside',
        'Serviços de emergência (Fora do Empreendimento Turístico da localidade mais próxima)': 'emergency_services_outside',
        'Outros Serviços Turísticos (Dentro do Recurso Turístico)': 'other_services_within',
        'Serviços básicos (Dentro do Recurso Turístico)': 'basic_services_within',
        'Imagens do recurso 2': 'feature_image_2',
        'Imagens do recurso 3': 'feature_image_3',
        'Imagens do recurso 4': 'feature_image_4',
        'Serviços de emergência (Dentro do Recurso Turístico)': 'emergency_services_within',
        'Acesso ao recurso (Marítimo)': 'maritime_access',
        'Nível atual de uso': 'current_usage_level',
        'Acesso ao recurso (Aéreo)': 'air_access',
        'Meio de viagem 2': 'travel_means_2'
    }
}
@st.cache_data
def cargar_dataset(idioma):
    ruta_archivo = f"data/santiago_cabo_verde_recursos_{idioma}.csv"
    if os.path.exists(ruta_archivo):
        df = pd.read_csv(ruta_archivo)
        # Aplicar el mapeo de columnas
        df = df.rename(columns=column_mappings[idioma])
        return df
    else:
        st.error(f"El archivo para el idioma {idioma} no existe.")
        return pd.DataFrame()

def cargar_traducciones(idioma):
    ruta = os.path.join("traducciones", f"{idioma}.json")
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            traducciones = json.load(f)
        return traducciones
    else:
        st.error(f"El archivo de traducciones para {idioma} no existe.")
        return {}

def obtener_idiomas():
    return [archivo.split(".")[0] for archivo in os.listdir("traducciones") if archivo.endswith(".json")]

def convertir_coordenadas(coordenadas):
    try:
        lat, lon = map(float, coordenadas.split(','))
        return lat, lon
    except ValueError:
        return None

def main():

    st.sidebar.image('assets/Logo_cabo_verde.png')
    
    idiomas_disponibles = obtener_idiomas()
    
    idioma_seleccionado = st.sidebar.selectbox(
        "Seleccione su idioma",
        idiomas_disponibles
    )

    # Cargar las traducciones para el idioma seleccionado
    traducciones = cargar_traducciones(idioma_seleccionado)
    
    # Cargar el dataset correspondiente y aplicar el mapeo de columnas
    datos = cargar_dataset(idioma_seleccionado)
    
    if datos.empty:
        st.error("No hay datos disponibles para este idioma.")
        return
    
    capas = {
        'OpenStreetMap': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        'Stamen Terrain': 'https://maps.stamen.com/terrain/{z}/{x}/{y}.jpg',
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
    capa_seleccionada = st.sidebar.selectbox(
        traducciones.get("seleccionar_capa", "Seleccionar capa"),
        list(capas.keys())
    )

    # Filtrar por isla
    ilha_seleccionada = st.sidebar.selectbox(
        traducciones.get("seleccionar_ilha", "Seleccionar isla"),
        ['Todos'] + sorted(datos['island'].dropna().unique())
    )
    
    # Filtrar los datos según la isla seleccionada
    if ilha_seleccionada != 'Todos':
        datos = datos[datos['island'] == ilha_seleccionada]

    # Filtrar por categoría
    categorias = sorted(datos['category'].dropna().unique())
    categorias_seleccionadas = st.sidebar.multiselect(
        traducciones.get("seleccionar_categorias", "Seleccionar categorías"),
        categorias,
        default=categorias
    )
    
    # Filtrar los datos según las categorías seleccionadas
    if categorias_seleccionadas:
        datos = datos[datos['category'].isin(categorias_seleccionadas)]

    # Crear el mapa utilizando Folium centrado en Cabo Verde
    mapa = folium.Map(
        location=[15.1111, -23.6167],  # Coordenadas aproximadas del centro de Cabo Verde
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

    # Añadir marcadores al mapa con identificadores únicos
    for index, fila in datos.iterrows():
        coordenadas = convertir_coordenadas(fila['lat_long'])
        if coordenadas:
            lat, lon = coordenadas
            nombre_recurso = fila['resource_name']
            popup = folium.Popup(nombre_recurso, max_width=250)
            folium.Marker(
                location=[lat, lon],
                popup=popup,
                tooltip=nombre_recurso,
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(mapa)
    

    salida = st_folium(mapa, width="100%")
            
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

    # CSS personalizado
    st.markdown(f"""
        <style>
            .stAppHeader {{
                display: none;
            }}
            .css-18e3th9 {{
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 0rem;
                padding-right: 0rem;
            }}
            .css-1d391kg {{
                padding-top: 0rem;
                padding-right: 0rem;
                padding-bottom: 0rem;
                padding-left: 0rem;
            }}
            .stAppToolbar {{
                display: none;
            }}
            .stMainBlockContainer {{
                padding: 0 !important;
                height: 1000%;
            }}
            .stElementContainer {{
                padding: 0 !important;
                margin-bottom: auto;
            }}
            .st-emotion-cache-1h9usn1{{
                background-color: white;
                padding: 40px;
                border-radius: 30px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                width: 90%;
                margin: 0 auto;
            }}
            .st-emotion-cache-8qhzib {{
                width: 652px;
                position: relative;
                display: flex;
                flex: 1 1 0%;
                flex-direction: column;
                gap: 0rem;
            }}
            .st-emotion-cache-dryeer {{
                width: auto;
                position: relative;
                display: block;
                flex-direction: column;
                gap: 0rem;
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