#Archivo de la lógica, es el cálculo de la compatibilidad de los inquilinos

#Primero se importan las librerias para trabajar
import numpy as np #Operaciones matemáticas
import pandas as pd #Manejar data sets y análisis de datos
from sklearn.preprocessing import OneHotEncoder #Libreria de manejo de datos de inteligencia artificial, y herramientas científicas

#Cargar los datos
df_inquilinos = pd.read_csv('dataset_inquilinos.csv', index_col='id_inquilino')
df_inquilinos

#Renombrar las columnas del dataset para mayor claridad
df_inquilinos.columns =['Horario', 'Bioritmo', 'Nivel Educativo', 'Lee', 'Animación', 'Cine', 
                        'Mascotas', 'Cocinar', 'Deporte', 'Dieta', 'Fumador',
                        'Visitas', 'Orden', 'Musica', 'Musica_alta', 'Plan_perfecto', 'Instrumento']

#Convertir las variables categoricas en representaciones binarios
encoder = OneHotEncoder(sparse_output=False)
df_encoder_inquilinos = encoder.fit_transform(df_inquilinos)

#Convertir df_encoded a DataFrame
encoded_nombres = encoder.get_feature_names_out()
#Convertir a data Frame de Pandas
df_encoded = pd.DataFrame(df_encoder_inquilinos, index=df_inquilinos.index, columns=encoded_nombres)

#Crear la matriz de similaridad que implementa el producto punto
#El producto punto es para determinar un grado de similaridad
matriz_sing = np.dot(df_encoder_inquilinos, df_encoder_inquilinos.T)

#Reescalar la matriz de similaridad para que se de en un rango definido
rango_min, rango_max = -100, 100
min_orginal, max_original = np.min(matriz_sing), np.max(matriz_sing)
#Calculo para reescalar la matriz
matriz_reescalada = ((matriz_sing - min_orginal) / (max_original - min_orginal)) * (rango_max - rango_min) + rango_min

#Convertir la matriz a dataframe
df_similaridad = pd.DataFrame(matriz_reescalada, index = df_inquilinos.index, columns=df_inquilinos.index)

#Función principal de búsqueda de compatibilidad
def inquilinos_compatibles(id_inquilinos, topn):
    #Validar los id en la matriz de similaridad
    for id_inquilino in id_inquilinos:
        #Buscar si los inquilinos están disponibles
        if id_inquilino not in df_encoder_inquilinos.index:
            return 'Falta uno de los inquilinos en la base de datos'
        
    #Obtener las filas correspondientes a los inquilinos
    filas_inquilinos = df_similaridad.loc[id_inquilinos]
    
    #Calcular la similitud promedio en los inquilinos
    similitud_promedio = filas_inquilinos.mean(axis=0)
    
    #Ordenar los inquilinos en función de su similitud promedio
    inquilinos_similares = similitud_promedio.sort_values(ascending=False)
    
    #Excluir los inquilinos de referencia
    topn_inquilinos = inquilinos_similares.head(topn)
    
    #Obtener los registros de inquilinos similares
    registros_similares = df_inquilinos.loc[topn_inquilinos.index]
    
    #Obtener los registros de los inquilinos buscados
    registros_buscados = df_inquilinos.loc[id_inquilinos]
    
    # Concatenar los registros buscados con los registros similares en las columnas
    resultado = pd.concat([registros_buscados.T, registros_similares.T], axis=1)

    # Crear un objeto Series con la similitud de los inquilinos similares encontrados
    similitud_series = pd.Series(data=pd.to_numeric(topn_inquilinos.values, errors='coerce'), index=topn_inquilinos.index, name='Similitud')

    # Devolver el resultado y el objeto Series
    return resultado, similitud_series
    


    