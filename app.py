#Importar las bibliotecas necesarias
import streamlit as st  #Para crear interfaces gráficas, dashborads interactivos, python para front-end
import pandas as pd
#Traernos de los módulos las funciones necesarias
from logica_negocio import inquilinos_compatibles
from ayudantes import generar_grafico_compatibilidad, obtener_id_inquilinos, generar_tabla_compatibilidad

#Configurar las dimensiones web de la página
st.set_page_config(layout="wide")

#Para ver el resultado, se necesita una variable para ir guardando los cambios
resultado = None

#Mostrar la portada
st.image(r'C:\Users\maria\OneDrive\Escritorio\Códigos\Habitaciones-inquilinos\habitaciones.png', use_container_width=True)

#Insertar un espacio vertical de 60px para mejorar la estética
st.markdown(f'<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)

#Configurar el sidebar con inputs y un boton
with st.sidebar:
    st.header("¿Quien está viviendo ya en el piso?")
    
    #Cajas de entrada para los IDS de los inquilinos actuales
    inquilino1 = st.text_input("Inquilino 1")
    inquilino2 = st.text_input("Inquilino 2")
    inquilino3 = st.text_input("Inquilino 3")
    
#Entrada para el número de compañeros buscados
num_compañeros = st.text_input("¿Cuántos compañeros buscas?")

#Botón para ejecutar la búsqueda
if st.button('Buscar nuevos compañeros'):
    try:
        #Convertir a entero el número de compañeros
        topn = int(num_compañeros)
    except ValueError:
        st.error('El número de compañeros no es válido')
        topn = None
    
    #Obtener los IDs de los inquilinos usando la función de ayuda
    id_inquilinos = obtener_id_inquilinos(inquilino1, inquilino2, inquilino3, topn)
    
    #Si se obtienen IDs válidos, ejecutar la función principal de búsqueda de compatibilidad
    if id_inquilinos and topn is not None:
        resultado = inquilinos_compatibles(id_inquilinos, topn)

#Mostrar mensajes de error si el resultado contiene mensajes de error
if isinstance(resultado, str):
    st.error(resultado)
#Si se obtienen resultados, mostrar el gráfico y la tabla
elif resultado is not None:
    cols = st.columns((1,2)) #Divide el layout en dos columnas
    
    #Primera columna para el gráfico de compatibilidad
    with cols[0]:
        st.write("Nivel de compatibilidad de cada compañero")
        
        #Verificar el tipo de resultado 
        st.write(f"Tipo de resultado[1]: {type(resultado[1])}")
        st.write(f"Contenido de resultado[1]: {resultado[1]}")
        st.write(resultado[1])
        
        try:
            fig_grafico = generar_grafico_compatibilidad(resultado[1])
            st.pyplot(fig_grafico)
        except TypeError as e:
            st.error(f"Error: {str(e)}")
    
    #Segunda columna para el gráfico de compatibilidad
    with cols[1]:
        st.write("Comparativa entre compañeros: ")
        fig_tabla = generar_grafico_compatibilidad(resultado)
        st.plotly_chart(fig_tabla, use_container_width=True)
    
        