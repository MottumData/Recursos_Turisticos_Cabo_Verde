'''
        if recurso is not None:
            # Crear un contenedor para el panel de detalles
            with st.container():
                with st.expander(traducciones.get("detalles_recurso", "Detalles del Recurso"), expanded=True):
                    cols = st.columns([3, 2])
                    
                    with cols[0]:
                        st.markdown(f"### {recurso['resource_name']}")
                        
                        # Información básica
                        info_basica = {
                            traducciones.get("council_label", "Consejo"): recurso.get('council', ''),
                            traducciones.get("parish_label", "Parroquia"): recurso.get('parish', ''),
                            traducciones.get("classification_label", "Clasificación"): recurso.get('classification', ''),
                            traducciones.get("village_label", "Aldea"): recurso.get('village', ''),
                            traducciones.get("neighborhood_label", "Vecindario"): recurso.get('neighborhood', '')
                        }
                    
                        for key, value in info_basica.items():
                            if value:
                                st.markdown(f"**{key}:** {value}")
                        
                        # Descripción del producto
                        descripcion = recurso.get('description', '')
                        if descripcion:
                            st.markdown(f"### {traducciones.get('descripcion', 'Descripción')}")
                            st.info(descripcion)
                        
                        # Elementos materiales asociados
                        elementos_materiales = recurso.get('material_elements', '')
                        if elementos_materiales:
                            st.markdown(f"### {traducciones.get('elementos_materiales', 'Elementos Materiales')}")
                            st.info(elementos_materiales)
                        
                        # Elementos naturales asociados
                        elementos_naturales = recurso.get('natural_elements', '')
                        if elementos_naturales:
                            st.markdown(f"### {traducciones.get('elementos_naturales', 'Elementos Naturales')}")
                            st.info(elementos_naturales)
                    
                    with cols[1]:
                        # Mostrar imágenes si están disponibles
                        for i in range(1, 5):
                            img_key = f'feature_image_{i}'
                            img_url = recurso.get(img_key, '')
                            if img_url and pd.notna(img_url):
                                st.image(img_url, use_column_width=True)
                                '''