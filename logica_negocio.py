import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Cargar los datos
df_inquilinos = pd.read_csv('dataset_inquilinos.csv', index_col='id_inquilino')

# Renombrar las columnas del dataset para mayor claridad
df_inquilinos.columns = [
    'Horario', 'Bioritmo', 'Nivel Educativo', 'Lee', 'Animación', 'Cine', 
    'Mascotas', 'Cocinar', 'Deporte', 'Dieta', 'Fumador',
    'Visitas', 'Orden', 'Musica', 'Musica_alta', 'Plan_perfecto', 'Instrumento'
]

# Convertir las variables categóricas en representaciones binarias
encoder = OneHotEncoder(sparse_output=False)
df_encoder_inquilinos = encoder.fit_transform(df_inquilinos)

# Convertir df_encoded a DataFrame
encoded_nombres = encoder.get_feature_names_out()
df_encoded = pd.DataFrame(df_encoder_inquilinos, index=df_inquilinos.index, columns=encoded_nombres)

# Crear la matriz de similaridad
matriz_sing = np.dot(df_encoder_inquilinos, df_encoder_inquilinos.T)

# Reescalar la matriz de similaridad en un rango de 0 a 100
rango_min, rango_max = 0, 100
min_original, max_original = np.min(matriz_sing), np.max(matriz_sing)
matriz_reescalada = ((matriz_sing - min_original) / (max_original - min_original)) * (rango_max - rango_min) + rango_min

# Convertir la matriz reescalada a DataFrame
df_similaridad = pd.DataFrame(matriz_reescalada, index=df_inquilinos.index, columns=df_inquilinos.index)

# Función principal de búsqueda de compatibilidad
def inquilinos_compatibles(id_inquilinos, topn):
    for id_inquilino in id_inquilinos:
        if id_inquilino not in df_encoded.index:
            return None  # Retornar None si algún inquilino no está en la base de datos
    
    #Hacer cálculos con Pandas para hacer los cálculos y el plot del proyecto
    #organizar por id el data frame
    filas_inquilinos = df_similaridad.loc[id_inquilinos]
    #Calcular la  media (similitud promedio)
    similitud_promedio = filas_inquilinos.mean(axis=0)
    #Organizar y limpiar la similtud promedio
    inquilinos_similares = similitud_promedio.sort_values(ascending=False).drop(id_inquilinos)
    
    #Si no tienen similitudes, retorna none
    if inquilinos_similares.empty:
        return None
    
    #Buscar el top de inquilinos compatibles con la búsqueda
    topn_inquilinos = inquilinos_similares.head(topn)
    #Buscar y organizar los registros similares
    registros_similares = df_inquilinos.loc[topn_inquilinos.index]
    #Buscar todos los registros que coincidan con una consulta
    registros_buscados = df_inquilinos.loc[id_inquilinos]
    
    #Unir el data frame de los buscados y los similares
    resultado = pd.concat([registros_buscados.T, registros_similares.T], axis=1)
    #Crear una serie con la similitud
    similitud_series = pd.Series(data=topn_inquilinos.values, index=topn_inquilinos.index, name='Similitud')
    
    #Devolver el resultado al app.py
    return resultado, similitud_series

    