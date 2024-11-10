#Importar las librerias
import os #Comandos del sistema operativo
os.system('cls') 
import matplotlib.pyplot as plt #Para hacer gráficas basadas en matemáticas
import pandas as pd
import seaborn as sns #Para hacer gráficas mas especializadoas
import plotly.graph_objs as go #Graficos interactivps
import streamlit as st #Para implementar aplicaciones web

#Función para generar el gráfico de compatibilidad
def generar_grafico_compatibilidad(compatibilidad):
    #Convertir 'compatibilidad a pd.Series si no es
    if not isinstance(compatibilidad, pd.Series):
        try: 
            compatibilidad = pd.Series(compatibilidad)
        except Exception as e:
            raise TypeError("La variable no es válida ")
    
    #Verificar 
    compatibilidad = pd.to_numeric(compatibilidad, errors= 'coerce')
    
    # Verificar si después de la conversión `compatibilidad` sigue teniendo valores válidos
    if compatibilidad.isna().all():
        raise TypeError("La variable 'compatibilidad' no contiene valores numéricos válidos después de la conversión.")
    
    
    #Eliminar valores NaN
    compatibilidad = compatibilidad.dropna()
    
    #Convertir los valores a porcentajes
    compatibilidad = compatibilidad / 100
    
    #Configurar el gráfico de barras con seaborn
    fig, ax = plt.subplots(figsize=(5,4))
    
    #Crear el gráfico de barras
    sns.barplot(x=compatibilidad.index, y=compatibilidad.values, ax=ax, color='green')
    
    #Configurar etiquetas, valores y ejes
    #Etiquetas
    ax.set_xlabel('ID inquilino', fontsize = 10)
    ax.set_ylabel('Similitud (%)', fontsize=10)
    
    #Hacer que los ejes coincidam
    ax.set_xticks(range(len(compatibilidad)))
    
    #Ejes y formato de las etiquetas
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_yticklabels(['{:.1f}%'.format(y * 100) for y in ax.get_yticks()], fontsize=8)
    
    #Añadir porcentaje de barras en cada barra
    for p in ax.patches:
        #Altura
        height = p.get_height()
        #Cambiar la escritura del eje
        ax.annotate('{:.1f}%'.format(height * 100),
                    (p.get_x() + p.get_width() /2., height),
                    #Ajustar la etiqueta del centro
                    ha = 'center', va='center',
                    #Ajustar la fuente de los textos
                    xytext=(0,5),
                    #Poner los nombres de los puntos de los ejes
                    textcoords='offset points', fontsize=8)
        
        return fig
        
#Función para generar la tabla de comparación
def generar_tabla_compatibilidad(resultado):
    #Agregar índice para los atributos y preparar la tabla
    resultado_0_with_index = resultado[0].reset_index()
    resultado_0_with_index.rename(columns={'index': 'ATRIBUTO'}, inplace=True)

    #Crear la tabla con Plotly para comparar los atributos
    fig_table = go.Figure(data=[go.Table(
                columnwidth=[20] + [10] *(len(resultado_0_with_index.columns) -1),
                header=dict(values=list(resultado_0_with_index.columns), fill_color='green', align='left'),
                cells=dict(values=[resultado_0_with_index[col] for col in resultado_0_with_index.columns],
                        fill_color='lavender', align='left')
                )])
    
    #Configurar el layout de la tabla
    fig_table.update_layout(width=700, height=320, margin=dict(l=0, r=0, t=0, b=0))
    return fig_table

#Función para validar el ID de los inquilinos
def obtener_id_inquilinos(inquilino1, inquilino2, inquilino3, topn):
    #Crear una lista para almacenar los IDs de los inquilinos ingresados
    id_inquilinos=[]
    #Recorrer la lista
    for inquilino in [inquilino1, inquilino2, inquilino3]:
        #Try except para manejar los errores de que no exista el inquilino
        try:
            if inquilino:
                #Convertir a entero y agregar a la lista
                id_inquilinos.append(int(inquilino))
        except ValueError:
            #Mostrar el mensaje de error si el valor no es válido
            st.error(f"El identificador del inquilino'{inquilino}' no es un identificador válido")
            id_inquilinos = []
            break
    return id_inquilinos
                                

