# Importar las bibliotecas necesarias
import streamlit as st
import pandas as pd
from logica_negocio import inquilinos_compatibles
from ayudantes import generar_grafico_compatibilidad, obtener_id_inquilinos, generar_tabla_compatibilidad

# Configurar las dimensiones web de la página
st.set_page_config(layout="wide")

# Para ver el resultado, se necesita una variable para ir guardando los cambios
resultado = None  # Asegurarse de que 'resultado' se inicializa como None

# Mostrar la portada
#Ajustar al tamaño de la página
st.image(r'./habitaciones.png', use_container_width=True)

# Insertar un espacio vertical de 60px para mejorar la estética
st.markdown(f'<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)

# Configurar el sidebar con inputs y un botón
with st.sidebar:
    st.header("¿Quién está viviendo ya en el piso?")
    
    # Cajas de entrada para los IDS de los inquilinos actuales
    inquilino1 = st.text_input("Inquilino 1")
    inquilino2 = st.text_input("Inquilino 2")
    inquilino3 = st.text_input("Inquilino 3")
    
# Entrada para el número de compañeros buscados
num_compañeros = st.text_input("¿Cuántos compañeros buscas?")

# Botón para ejecutar la búsqueda
if st.button('Buscar nuevos compañeros'):
    try:
        # Convertir a entero el número de compañeros
        topn = int(num_compañeros)
    except ValueError:
        st.error('El número de compañeros no es válido')
        topn = None
    
    # Obtener los IDs de los inquilinos usando la función de ayuda
    id_inquilinos = obtener_id_inquilinos(inquilino1, inquilino2, inquilino3, topn)
    
    # Si se obtienen IDs válidos, ejecutar la función principal de búsqueda de compatibilidad
    if id_inquilinos and topn is not None:
        resultado = inquilinos_compatibles(id_inquilinos, topn)
    else:
        resultado = None

# Verificar si el resultado es válido y mostrar el gráfico y la tabla
if resultado is not None and isinstance(resultado, tuple) and len(resultado) == 2:
    cols = st.columns((1, 2))

    # Primera columna para el gráfico de compatibilidad
    with cols[0]:
        st.write("Nivel de compatibilidad de cada compañero")
        
        # Verificar si resultado[1] es una Serie válida y contiene valores numéricos
        if isinstance(resultado[1], pd.Series):
            compatibilidad = pd.to_numeric(resultado[1], errors='coerce').dropna()

            if not compatibilidad.empty:
                try:
                    # Generar el gráfico si hay datos válidos
                    fig_grafico = generar_grafico_compatibilidad(compatibilidad)
                    if fig_grafico is not None:
                        st.pyplot(fig_grafico)
                    else:
                        st.error("No se pudo generar el gráfico de compatibilidad debido a datos insuficientes.")
                except TypeError as e:
                    st.error(f"Error al generar el gráfico: {str(e)}")
            else:
                st.error("No se encontraron valores numéricos válidos para generar el gráfico de compatibilidad.")
        else:
            st.error("Resultado no tiene el formato esperado.")

    # Segunda columna para la tabla de comparación
    with cols[1]:
        st.write("Comparativa entre compañeros")
        
        try:
            fig_tabla = generar_tabla_compatibilidad(resultado)
            if fig_tabla is not None:
                st.plotly_chart(fig_tabla, use_container_width=True)
            else:
                st.error("No se pudo generar la tabla de comparación debido a datos insuficientes.")
        except Exception as e:
            st.error(f"Error al generar la tabla de comparación: {str(e)}")
else:
    if resultado is None:
        st.error("No se encontraron inquilinos compatibles o hubo un error en la búsqueda.")
