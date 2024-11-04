import folium

def crear_mapa(datos):
    mapa = folium.Map(location=[datos['Latitud'].mean(), datos['Longitud'].mean()], zoom_start=10)
    for _, fila in datos.iterrows():
        folium.Marker([fila['Latitud'], fila['Longitud']], popup=fila['nombre']).add_to(mapa)
    return mapa