import streamlit as st
import pandas as pd  # Asegúrate de importar pandas
from src.data_utils import cargar_dataset, cargar_traducciones

def main():
    st.set_page_config(page_title="Detalle del Recurso", layout="wide")

    # Obtener el resource_id desde st.session_state
    resource_id = st.session_state.get('resource_id', None)

    if resource_id is None:
        st.error("No se ha seleccionado un recurso.")
        return

    # Cargar los datos
    idioma_seleccionado = st.session_state.get('idioma_seleccionado', 'es')
    datos = cargar_dataset(idioma_seleccionado)

    if datos.empty:
        st.error("No hay datos disponibles.")
        return

    # Obtener detalles del recurso
    try:
        detalle = datos[datos['id'] == int(resource_id)].iloc[0]
    except IndexError:
        st.error("Recurso no encontrado.")
        return

    # Mostrar detalles
    st.header(detalle['resource_name'])

    cols = st.columns([3, 2])

    with cols[0]:
        st.markdown(f"**Consejo:** {detalle.get('council', 'N/A')}")
        st.markdown(f"**Parroquia:** {detalle.get('parish', 'N/A')}")
        st.markdown(f"**Clasificación:** {detalle.get('classification', 'N/A')}")
        st.markdown(f"**Aldea:** {detalle.get('village', 'N/A')}")
        st.markdown(f"**Vecindario:** {detalle.get('neighborhood', 'N/A')}")
        st.markdown("### Descripción")
        st.write(detalle.get('description', 'N/A'))
        st.markdown("### Elementos Materiales")
        st.write(detalle.get('material_elements', 'N/A'))
        st.markdown("### Elementos Naturales")
        st.write(detalle.get('natural_elements', 'N/A'))

    with cols[1]:
        for i in range(1, 5):
            img_key = f'feature_image_{i}'
            img_url = detalle.get(img_key, '')
            if img_url and pd.notna(img_url):
                st.image(img_url, use_column_width=True)

    # Botón para volver al mapa
    if st.button("Volver al Mapa"):
        st.session_state.pop('resource_id', None)
        st.experimental_switch_page("app")

if __name__ == "__main__":
    main()