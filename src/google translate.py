import pandas as pd
from googletrans import Translator

# Cargar el dataset original
datos = pd.read_csv('data/santiago_cabo_verde_recursos.csv')

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
idiomas = ['en', 'es']  # Agrega los códigos de idioma que necesites

# Columnas que deseas traducir
columnas_a_traducir = [
    'Nome do recurso turístico',
    'Classificação',
    'Cara',
    'Descrição do produto',
    'Elementos materiais associados',
    'Elementos naturais associados',
    'Acesso ao Recurso [Domínio público ou privado]',
    'Dados pendentes de interesse turístico',
    'Singularidade que o diferencia dos demais da região',
    'Possibilidades de exploração futura',
    'Intervenções necessárias para seu uso',
    'Acesso ao recurso (Terra)',
    'Meio de viagem',
    'Sinalização (Dentro do município)',
    'Sinalização (Fora do município)',
    'Sinalização (Na proximidade)',
    'Tipo de renda',
    'Aplica (Dentro do Recurso Turístico)',
    'Aplica (Fora do Recurso Turístico)',
    'ID',
    'Estado de conservação',
    'Outros Serviços Turísticos (Fora do Empreendimento Turístico da localidade mais próxima)',
    'Serviços Básicos ( Fora do Empreendimento Turístico da localidade mais próxima)',
    'Serviços de emergência (Fora do Empreendimento Turístico da localidade mais próxima)',
    'Outros Serviços Turísticos (Dentro do Recurso Turístico)',
    'Serviços básicos (Dentro do Recurso Turístico)',
    'Serviços de emergência (Dentro do Recurso Turístico)',
    'Acesso ao recurso (Marítimo)',
    'Nível atual de uso',
    'Acesso ao recurso (Aéreo)',
    'Meio de viagem 2'
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
    datos_traducidos_idioma.to_csv(f'data/santiago_cabo_verde_recursos_{idioma}.csv', index=False)
    print(f"Dataset traducido al idioma '{idioma}' guardado exitosamente.\n")