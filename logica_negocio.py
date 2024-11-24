import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity

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

# Calcular la similaridad utilizando la similaridad coseno
df_similaridad = pd.DataFrame(cosine_similarity(df_encoder_inquilinos),
                              index=df_inquilinos.index,
                              columns=df_inquilinos.index)

# Función principal de búsqueda de compatibilidad
def inquilinos_compatibles(id_inquilinos, topn):
    for id_inquilino in id_inquilinos:
        if id_inquilino not in df_similaridad.index:
            return None  # Retornar None si algún inquilino no está en la base de datos
        
    filas_inquilinos = df_similaridad.loc[id_inquilinos]
    similitud_promedio = filas_inquilinos.mean(axis=0)
    inquilinos_similares = similitud_promedio.sort_values(ascending=False).drop(id_inquilinos)
    
    if inquilinos_similares.empty:
        return None
    
    topn_inquilinos = inquilinos_similares.head(topn)
    registros_similares = df_inquilinos.loc[topn_inquilinos.index]
    registros_buscados = df_inquilinos.loc[id_inquilinos]
    
    resultado = pd.concat([registros_buscados.T, registros_similares.T], axis=1)
    similitud_series = pd.Series(data=topn_inquilinos.values, index=topn_inquilinos.index, name='Similitud')
    
    return resultado, similitud_series
