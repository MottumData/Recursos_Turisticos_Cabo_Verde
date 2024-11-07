import streamlit as st
import pandas as pd
import folium
from folium import plugins
from streamlit_folium import st_folium

# Configura la página para que use el diseño ancho
st.set_page_config(layout="wide")

def convertir_coordenadas(coordenadas):
    try:
        lat, lon = map(float, coordenadas.split(','))
        return lat, lon
    except ValueError:
        return None

def main():

    st.sidebar.image('assets/Instituto_do_turismo.png')
    
    capas = {
        'OpenStreetMap': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        'Stamen Terrain': 'https://maps.stamen.com/terrain/{z}/{x}/{y}.jpg',
        'Stamen Toner': 'http://tile.stamen.com/toner/{z}/{x}/{y}.png',
        'CartoDB positron': 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
        'CartoDB dark_matter': 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
    }
    atribuciones = {
        'OpenStreetMap': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        'Stamen Terrain': 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under ODbL.',
        'Stamen Toner': 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under ODbL.',
        'CartoDB positron': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        'CartoDB dark_matter': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
    }
    capa_seleccionada = st.sidebar.selectbox(
        'Seleccione una capa del mapa:',
        list(capas.keys())
    )

    # Carga los datos desde el archivo CSV
    ruta_archivo = 'data/santiago_cabo_verde_recursos.csv'
    datos = pd.read_csv(ruta_archivo)
    
    if 'Cara' not in datos.columns:
        st.error("La columna 'Cara' no existe en el archivo CSV.")
        return
    
    # Reemplaza el radio button por un selectbox para 'ilha'
    ilha_seleccionada = st.sidebar.selectbox(
        'Selecione uma ilha:',
        ['Todos'] + sorted(datos['ilha'].unique())
    )

    # Filtrar los datos según la isla seleccionada
    if ilha_seleccionada != 'Todos':
        datos = datos[datos['ilha'] == ilha_seleccionada]

    # Reemplaza los checkboxes por un multiselect para 'Conselho'
    consejos = sorted(datos['Conselho'].unique())
    consejos_seleccionados = st.sidebar.multiselect(
        'Seleccione Conselhos:',
        consejos,
        # Selecciona todos por defecto
    )

    # Filtrar los datos según los Conselhos seleccionados
    if consejos_seleccionados:
        datos = datos[datos['Conselho'].isin(consejos_seleccionados)]
        
    categorias = ['Todos'] + sorted(datos['Cara'].unique())
    categoria_seleccionada = st.sidebar.radio(
        'Seleccione una categoría:',
        categorias
    )

    # Filtrar los datos según la categoría seleccionada
    if categoria_seleccionada != 'Todos':
        datos = datos[datos['Cara'] == categoria_seleccionada]

    # Crea el mapa utilizando Folium centrado en Cabo Verde
    mapa = folium.Map(
        location=[15.1111, -23.6167],  # Coordenadas aproximadas del centro de Cabo Verde
        zoom_start=10,
        tiles=capa_seleccionada,
    )

    plugins.Fullscreen(                                                         
            position = "topright",                                   
            title = "Open full-screen map",                       
            title_cancel = "Close full-screen map",                      
            force_separate_button = True,                                         
        ).add_to(mapa) 

    # Añade marcadores al mapa con identificadores únicos
    for index, fila in datos.iterrows():
        coordenadas = convertir_coordenadas(fila['Lat-Long'])
        if coordenadas:
            lat, lon = coordenadas
            popup = folium.Popup(fila['Nome do recurso turístico'], max_width=250)
            folium.Marker(
                location=[lat, lon],
                popup=popup,
                tooltip=fila['Nome do recurso turístico'],
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(mapa)

    # Muestra el mapa y captura los eventos de clic
    salida = st_folium(mapa, width="full-width")
    
    if salida is not None and salida.get('last_object_clicked'):
        lat = salida['last_object_clicked']['lat']
        lng = salida['last_object_clicked']['lng']
        
        # Encuentra el recurso más cercano a las coordenadas clickeadas
        recurso = None
        for _, fila in datos.iterrows():
            coords = convertir_coordenadas(fila['Lat-Long'])
            if coords and abs(coords[0] - lat) < 0.0001 and abs(coords[1] - lng) < 0.0001:
                recurso = fila
                break
        
        if recurso is not None:
            # Crear un contenedor para el panel de detalles
            with st.container():
                with st.expander("🏛️ Detalles del Recurso", expanded=False):
                    cols = st.columns([3, 2])
                    
                    with cols[0]:
                        st.markdown(f"### {recurso['Nome do recurso turístico']}")
                        
                        with st.container():# Información básica en una tabla
                            info_basica = {
                                "Concelho": recurso['Conselho'],
                                "Freguesia": recurso['Freguesia'],
                                "Classificação": recurso['Classificação'],
                                "Vila": recurso.get('Vila', ''),
                                "Bairro": recurso.get('Bairro', '')
                            }
                        
                        for key, value in info_basica.items():
                            if value:
                                st.markdown(f"**{key}:** {value}")
                        
                        if 'Descrição do produto' in recurso:
                            st.markdown("### 📝 Descripción")
                            st.info(recurso['Descrição do produto'])
                            
                        # Información adicional
                        if recurso.get('Elementos materiais associados'):
                            st.markdown("### 🏺 Elementos Materiales")
                            st.info(recurso['Elementos materiais associados'])
                        
                        if recurso.get('Elementos naturais associados'):
                            st.markdown("### 🌿 Elementos Naturales")
                            st.info(recurso['Elementos naturais associados'])
                    
                    with cols[1]:
                        # Mostrar imágenes si están disponibles
                        for i in range(1, 5):
                            img_key = f'Imagens do recurso {i}'
                            if img_key in recurso and pd.notna(recurso[img_key]):
                                st.image(recurso[img_key], use_column_width=True)
    
    st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                }
               .css-1d391kg {
                    padding-top: 0rem;
                    padding-right: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 0rem;
                }
                /* Oculta el encabezado y la barra de herramientas */
                header, .stAppToolbar {
                    display: none;
                }
                /* Oculta el encabezado y la barra de herramientas */
                header, .stAppHeader {
                    display: none;
                }
                /* Ajusta el padding y el margen del contenedor principal */
                .stMainBlockContainer {
                    padding: 0 !important;
                    margin: 0 !important;
                   /* overflow: hidden; */
                }
                .st-emotion-cache-1h9usn1{
                        background-color: white;
                        padding: 40px;
                        border-radius: 30px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        width: 90%;
                        margin: 0 auto;
                }
                .st-emotion-cache-8qhzib {
                    width: 652px;
                    position: relative;
                    display: flex;
                    flex: 1 1 0%;
                    flex-direction: column;
                    gap: 0rem;
                }
                #map_div .leaflet-container {
                    height: 100vh !important;
                }
                .stElementContainer {
                    padding: 0 !important;
                    margin-bottom: 0 !important;
                }
                .footer {
                    display: none;
                }
                .st-emotion-cache-bm2z3a{
                }
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()