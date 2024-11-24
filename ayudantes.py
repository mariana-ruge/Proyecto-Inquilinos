import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.graph_objs as go
import streamlit as st

# Función para generar el gráfico de compatibilidad
def generar_grafico_compatibilidad(compatibilidad):
    # Convertir a valores numéricos y eliminar NaN
    compatibilidad = pd.to_numeric(compatibilidad, errors='coerce').dropna()

    if compatibilidad.empty:
        raise TypeError("No hay suficientes datos numéricos para generar el gráfico.")

    # Normalizar valores a una escala de 0 a 1 para representar porcentajes
    compatibilidad = compatibilidad / 100

    fig, ax = plt.subplots(figsize=(5, 4))
    sns.barplot(x=compatibilidad.index, y=compatibilidad.values, ax=ax, color='green')
    
    # Configurar etiquetas y valores de los ejes
    ax.set_xlabel('ID inquilino', fontsize=10)
    ax.set_ylabel('Similitud (%)', fontsize=10)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_yticklabels(['{:.0f}%'.format(y * 100) for y in ax.get_yticks()], fontsize=8)

    # Añadir etiquetas con el porcentaje sobre cada barra
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{height * 100:.1f}%',
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='center',
                    xytext=(0, 5), textcoords='offset points', fontsize=8)

    return fig

# Función para generar la tabla de comparación
def generar_tabla_compatibilidad(resultado):
    # Cambiar el nombre de la columna 'index' y ajustar el ancho de las columnas
    resultado_0_with_index = resultado[0].reset_index()
    resultado_0_with_index.rename(columns={'index': 'ATRIBUTO'}, inplace=True)
    
    # Configurar la tabla de Plotly
    fig_table = go.Figure(data=[go.Table(
        columnwidth=[20] + [10] * (len(resultado_0_with_index.columns) - 1),
        header=dict(values=list(resultado_0_with_index.columns),
                    fill_color='green',
                    align='left'),
        cells=dict(values=[resultado_0_with_index[col] for col in resultado_0_with_index.columns],
                   fill_color='lavender',
                   align='left'))
    ])
    
    # Configurar el layout de la tabla de Plotly
    fig_table.update_layout(
        width=700, height=320,  # Ajustar según tus necesidades
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig_table

# Función para validar el ID de los inquilinos
def obtener_id_inquilinos(inquilino1, inquilino2, inquilino3, topn):
    # Crear una lista para almacenar los IDs de los inquilinos ingresados
    id_inquilinos = []
    # Recorrer la lista
    for inquilino in [inquilino1, inquilino2, inquilino3]:
        # Try except para manejar los errores de que no exista el inquilino
        try:
            if inquilino:
                # Convertir a entero y agregar a la lista
                id_inquilinos.append(int(inquilino))
        except ValueError:
            # Mostrar el mensaje de error si el valor no es válido
            st.error(f"El identificador del inquilino '{inquilino}' no es un identificador válido")
            id_inquilinos = []
            break
    return id_inquilinos
