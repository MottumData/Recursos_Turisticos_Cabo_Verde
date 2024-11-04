# Mapa Interactivo con Datos de Excel

Este proyecto es una aplicación interactiva que muestra un mapa con localizaciones en Santiago, Cabo Verde, utilizando datos de un archivo CSV. La aplicación permite filtrar las localizaciones por nombre y visualizar los datos en un mapa utilizando Folium.

## Requisitos

- Python 3.11
- Las librerías listadas en `requirements.txt`

## Instalación

1. Clona el repositorio:
    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2. Crea un entorno virtual y actívalo:
    ```sh
    python -m venv mapa_recursos
    source mapa_recursos/Scripts/activate  # En Windows
    # o
    source mapa_recursos/bin/activate  # En Unix o MacOS
    ```

3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

1. Ejecuta la aplicación:
    ```sh
    streamlit run app.py
    ```

2. Abre tu navegador web y ve a `http://localhost:8501` para ver la aplicación.

## Archivos Principales

- `app.py`: Archivo principal que ejecuta la aplicación Streamlit.
- `data/santiago_cabo_verde_localizaciones.csv`: Archivo CSV con las localizaciones.
- `src/cargar_datos.py`: Contiene la función [`cargar_datos`](src/cargar_datos.py) para cargar los datos desde el archivo CSV.
- `src/crear_mapa.py`: Contiene la función [`crear_mapa`](src/crear_mapa.py) para crear el mapa con Folium.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que desees realizar.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.