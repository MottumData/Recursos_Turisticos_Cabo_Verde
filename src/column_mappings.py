import os
import json
import streamlit as st

def cargar_column_mappings():
    # Obtener la ruta absoluta del archivo JSON
    ruta = os.path.join(os.path.dirname(__file__), "column_mappings.json")
    
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            mappings = json.load(f)
        return mappings
    else:
        st.error("El archivo column_mappings.json no existe.")
        return {}