import pandas as pd
from googletrans import Translator

# Cargar el dataset original
datos = pd.read_csv('data/rutas_cabo_verde.csv')
datos['id'] = datos.index + 1

translator = Translator()

def traducir_texto(texto, dest_idioma):
    if pd.isna(texto):
        return texto
    try:
        traduccion = translator.translate(str(texto), dest=dest_idioma)
        return traduccion.text
    except Exception as e:
        print(f"Error al traducir '{texto}': {e}")
        return texto

# Lista de idiomas a los que deseas traducir (ejemplo: inglés 'en' y español 'es')
idiomas = ['en', 'es', 'pt']  # Agrega los códigos de idioma que necesites

# Columnas que deseas traducir
columnas_a_traducir = [
    'Nombre de la ruta',
    'Municipios por los que transcurre',
    'URL_img1',
    'URL_img2',
    'URL_img3',
    'URL_img4',
    'Descripción de la ruta',
    'Duración',
    'Distancia',
    'Modo de acceso',
    'Dificultad',
    'Actividad',
    'Recursos incluidos',
    'Punto de inicio',
    'Punto de salida',
    'URL Google Maps',
    'Ruta LatLong Transformed',
    'Actividades Opcionales:',
    'Recomendaciones'
]

# Crear un diccionario para almacenar las traducciones de los nombres de columnas por idioma
nombres_columnas_traducidos = {idioma: {} for idioma in idiomas}

# Traducción de nombres de columnas
for idioma in idiomas:
    print(f"Traduciendo nombres de columnas al idioma '{idioma}'...")
    for columna in datos.columns:
        traduccion_columna = traducir_texto(columna, idioma)
        nombres_columnas_traducidos[idioma][columna] = traduccion_columna
    print(f"Nombres de columnas traducidos al idioma '{idioma}'\n")

# Traducción de valores en columnas de texto
for idioma in idiomas:
    print(f"Procesando traducciones para el idioma '{idioma}'")
    datos_traducidos_idioma = datos.copy()

    # Traducir los nombres de las columnas
    datos_traducidos_idioma.columns = [nombres_columnas_traducidos[idioma][col] for col in datos.columns]

    # Traducir los valores de las columnas seleccionadas
    for columna in columnas_a_traducir:
        if columna not in datos.columns:
            print(f"Columna '{columna}' no encontrada en el dataset original. Saltando...")
            continue
        print(f"Traduciendo columna '{columna}' al idioma '{idioma}'")
        columna_traducida = nombres_columnas_traducidos[idioma][columna]
        
        # Obtener valores únicos para optimizar
        valores_unicos = datos[columna].dropna().unique()
        traducciones = {}
        for valor in valores_unicos:
            traducciones[valor] = traducir_texto(valor, idioma)
        
        # Mapear las traducciones
        datos_traducidos_idioma[columna_traducida] = datos[columna].map(traducciones)
        print(f"Columna '{columna}' traducida al idioma '{idioma}'\n")

    # Guardar el DataFrame traducido
    datos_traducidos_idioma.to_csv(f'data/rutas_cabo_verde_{idioma}.csv', index=False)
    print(f"Dataset traducido al idioma '{idioma}' guardado exitosamente.\n")