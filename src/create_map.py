import folium
from folium import plugins
from src.draw_routes import convertir_coordenadas, procesar_rutas
import streamlit_folium as st_folium

def crear_mapa(datos, traducciones):

    mapa = folium.Map(
        location=[13.4000, -23.6167],
        zoom_start=9,
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
            {mas_informacion}
            '''

            # Agregar el marcador al mapa con el popup modificado
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=nombre_recurso,
                icon=folium.Icon(color=icono['color'], icon=icono['icon'], prefix='fa')
            ).add_to(mapa)

    return mapa