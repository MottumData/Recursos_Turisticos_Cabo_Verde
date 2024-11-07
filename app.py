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

    # Carga los datos desde el archivo CSV
    ruta_archivo = 'data/santiago_cabo_verde_recursos.csv'
    datos = pd.read_csv(ruta_archivo)
    
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
        consejos
        # Selecciona todos por defecto
    )

    # Filtrar los datos según los Conselhos seleccionados
    if consejos_seleccionados:
        datos = datos[datos['Conselho'].isin(consejos_seleccionados)]
    else:
        # Si no se selecciona ningún consejo, vacía el DataFrame
        datos = datos.iloc[0:0]

    # Crea el mapa utilizando Folium centrado en Cabo Verde
    mapa = folium.Map(
        location=[15.1111, -23.6167],  # Coordenadas aproximadas del centro de Cabo Verde
        zoom_start=10
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

    # Si se hace clic en un marcador, muestra la información debajo del mapa
    if salida.get('last_object_clicked') is not None:
        lat_clicked = salida['last_object_clicked']['lat']
        lon_clicked = salida['last_object_clicked']['lng']
        # Filtra el DataFrame para obtener el recurso seleccionado
        delta = 1e-5  # Margen de tolerancia
        recurso_seleccionado = datos[
            (abs(datos['latitude'] - lat_clicked) < delta) &
            (abs(datos['longitude'] - lon_clicked) < delta)
        ]
        if not recurso_seleccionado.empty:
            st.markdown("---")
            nombre_recurso = recurso_seleccionado.iloc[0]['Nome do recurso turístico']
            st.subheader(f"Información de {nombre_recurso}")
            # Mostrar la información del recurso de forma ordenada
            for columna in recurso_seleccionado.columns:
                if columna not in ['latitude', 'longitude', 'Lat-Long']:
                    valor = recurso_seleccionado.iloc[0][columna]
                    st.write(f"**{columna}:** {valor}")
    # Aplica CSS para que el contenedor del mapa ocupe todo el espacio disponible
    
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
                }
        </style>
        """, unsafe_allow_html=True)

    # Muestra los datos cargados
    st.write('Datos cargados:')
    st.dataframe(datos)

if __name__ == "__main__":
    main()