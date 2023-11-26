import pandas as pd
from fastapi import FastAPI, HTTPException
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from typing import List


app = FastAPI()

#Archivos para consumirse en la api
games=pd.read_parquet("../DataSets/steam_games.parquet")
developer_opinion=pd.read_parquet("../Funciones/developer_opinion.parquet")
user_items=pd.read_parquet("../DataSets/user_items.parquet")
playtime=pd.read_parquet("../Funciones/playtime.parquet")
modelo_final=pd.read_parquet("../DatosML/ModeloFinal.parquet")




#Primera función



# Primera función
def validate_genre(genre):
    genre_name = genre.capitalize()
    df_filtered = games[games['genres'].str.contains(genre, case=False, na=False)]
    if df_filtered.empty:
        raise HTTPException(status_code=404, detail=f"Género {genre_name} no encontrado")

@app.get('/UserForGenre')
def user_for_genre(genre: str):
    """
    Obtiene el usuario con más horas jugadas para un género dado.
    """
    validate_genre(genre)

    genre_name = genre.capitalize()
    df_filtered = games[games['genres'].str.contains(genre, case=False, na=False)]

    df_merged = pd.merge(playtime, df_filtered[['id', 'release_date']], left_on='item_id', right_on='id')
    user_with_most_playtime = df_merged.groupby('user_id')['playtime_forever'].sum().idxmax()
    playtime_by_year = df_merged.groupby(['release_date', 'user_id'])['playtime_forever'].sum().reset_index()
    playtime_by_year = playtime_by_year[playtime_by_year['user_id'] == user_with_most_playtime]
    playtime_by_year = playtime_by_year.rename(columns={'release_date': 'Año', 'playtime_forever': 'Horas'})

    result = {
        f"Usuario con más horas jugadas para Género {genre_name}": user_with_most_playtime,
        "Horas jugadas": [{"Año": str(row['Año']), "Horas": row['Horas']} for _, row in playtime_by_year.iterrows()]
    }
    return result



#Segunda función


# Validar año
def validate_year(year):
    if year not in developer_opinion['release_date'].unique():
        raise HTTPException(status_code=404, detail=f"Año {year} no encontrado")

# Obtener top 3 de juegos MÁS recomendados
@app.get('/UsersRecommend', response_model=List[dict])
def users_recommend(year: int):
    """
    Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.
    """
    validate_year(year)

    # Filtrar reseñas para el año y con recomendación positiva
    df_filtered = developer_opinion[(developer_opinion['release_date'] == year) & (developer_opinion['recommend'] == True)]

    # Ordenar por puntuación positiva en orden descendente y tomar las primeras 3
    df_sorted = df_filtered.sort_values(by='Positivo', ascending=False).head(3)

    # Crear el resultado con el formato especificado
    result = [{"Puesto {}".format(i+1): {"Título": title, "Puntuación Positiva": positive_score}} for i, (title, positive_score) in enumerate(zip(df_sorted['title'], df_sorted['Positivo']))]
    
    return result



#Tercera Función
# Validar año
def validate_year(year):
    if year not in developer_opinion['release_date'].unique():
        raise HTTPException(status_code=404, detail=f"Año {year} no encontrado")

# Obtener top 3 de desarrolladoras con juegos MENOS recomendados
@app.get('/UsersWorstDeveloper', response_model=List[dict])
def users_worst_developer(year: int):
    """
    Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado.
    """
    validate_year(year)

    # Filtrar reseñas para el año y con recomendación negativa
    df_filtered = developer_opinion[(developer_opinion['release_date'] == year) & (developer_opinion['sentiment_analisis'].isin([0, 1, 2]))]

    # Agrupar por desarrolladora y contar las reseñas por categoría
    df_grouped = df_filtered.groupby(['developer', 'sentiment_analisis'])['sentiment_analisis'].count().unstack(fill_value=0).reset_index()

    # Renombrar las columnas
    df_grouped.columns = ['developer', 'Neutral', 'Negativo', 'Positivo']

    # Ordenar por puntos negativos en orden descendente y tomar las primeras 3
    df_sorted = df_grouped.sort_values(by='Negativo', ascending=False).head(3)

    # Crear el resultado con el formato especificado
    result = [{"Puesto {}".format(i+1): {"Desarrolladora": developer, "Puntuación Negativa": negative_points}} for i, (developer, negative_points) in enumerate(zip(df_sorted['developer'], df_sorted['Negativo']))]
    
    return result




#cuarta función 
@app.get('/sentiment_analysis')
def sentiment_analysis(developer: str):
    """
    Devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros
    de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.
    """
    # Convertir la columna 'developer' a str y filtrar valores nulos o extraños
    df_filtered = developer_opinion[developer_opinion['developer'].notnull()]
    df_filtered['developer'] = df_filtered['developer'].astype(str)

    # Filtrar por desarrolladora
    df_filtered = df_filtered[df_filtered['developer'] == developer]

    if df_filtered.empty:
        raise HTTPException(status_code=404, detail=f"Desarrolladora '{developer}' no encontrada")

    # Realizar el análisis de sentimiento
    sentiment_counts = df_filtered['sentiment_analisis'].value_counts().to_dict()

    # Ajustar el resultado para reflejar que 2 es positivo, 0 es neutral y 1 es negativo
    adjusted_sentiments = {2: "Positivo", 0: "Neutral", 1: "Negativo"}
    sentiment_counts = {adjusted_sentiments[key]: value for key, value in sentiment_counts.items()}

    result = {developer: sentiment_counts}
    return result



#Modelo de recomendación 
def encontrar_juegos_similares(id_juego: int) -> List[str]:
    """
    Encuentra juegos similares a un juego dado por su ID.

    Parameters:
    - id_juego: ID del juego para el cual se desean encontrar juegos similares.

    Returns:
    - Lista de nombres de juegos similares.
    """
    # Encuentra el índice del juego ingresado por ID
    juego_indice = modelo_final.index[modelo_final['id'] == id_juego].tolist()

    # Verifica si el juego con el ID especificado existe en la base de datos
    if not juego_indice:
        raise HTTPException(status_code=404, detail=f"El juego con el ID {id_juego} no existe en la base de datos.")

    juego_indice = juego_indice[0]

    # Extrae las características del juego ingresado
    juego_caracteristicas = modelo_final.iloc[juego_indice, 3:].values.reshape(1, -1)

    # Calcula la similitud coseno entre el juego ingresado y todos los demás juegos
    similitudes_render = cosine_similarity(modelo_final.iloc[:, 3:], juego_caracteristicas)

    # Obtiene los índices de los juegos más similares (excluyendo el juego de entrada)
    indices_juegos_similares = similitudes_render.argsort(axis=0)[::-1][1:6].flatten()[1:]

    # Obtiene los juegos más similares en función de los índices
    juegos_similares = modelo_final.iloc[indices_juegos_similares]['title'].tolist()

    return juegos_similares

# Decorador y endpoint para la función encontrar_juegos_similares
@app.get('/encontrar-juegos-similares/{id_juego}', response_model=List[str])
def encontrar_juegos_similares_endpoint(id_juego: int):
    return encontrar_juegos_similares(id_juego)