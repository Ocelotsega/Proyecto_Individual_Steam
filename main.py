from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from typing import List



app = FastAPI()



#Archivos para consumirse en la api
games=pd.read_parquet("DataSets/steam_games.parquet")
developer_opinion=pd.read_parquet("Funciones/developer_opinion.parquet")
playtime=pd.read_parquet("Funciones/playtime.parquet")
modelo_final=pd.read_parquet("DatosML/ModeloFinal.parquet")




@app.get("/", response_class=HTMLResponse)
async def inicio():
    template = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>API Steam</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                p {
                    color: #666;
                    text-align: center;
                    font-size: 18px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>API Consultas</h1>
        </body>
    </html>
    """
   
    return HTMLResponse(content=template)








# Primera función optimizada
@app.get('/UserForGenre')
def user_for_genre(genre: str):
    """
    Obtiene el usuario con más horas jugadas para un género dado.
    """

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
    return JSONResponse(content=result)

@app.get('/UsersRecommend')
def users_recommend(year: int):
    """
    Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.
    """

    df_filtered = developer_opinion[(developer_opinion['release_date'] == year) & (developer_opinion['recommend'] == True)]
    df_sorted = df_filtered.sort_values(by='Positivo', ascending=False).head(3)

    result = [{"Puesto {}".format(i+1): {"Título": title, "Puntuación Positiva": positive_score}} for i, (title, positive_score) in enumerate(zip(df_sorted['title'], df_sorted['Positivo']))]
    
    return JSONResponse(content=result)

@app.get('/UsersWorstDeveloper')
def users_worst_developer(year: int):
    """
    Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado.
    """

    df_filtered = developer_opinion[(developer_opinion['release_date'] == year) & (developer_opinion['sentiment_analisis'].isin([0, 1, 2]))]
    df_grouped = df_filtered.groupby(['developer', 'sentiment_analisis'])['sentiment_analisis'].count().unstack(fill_value=0).reset_index()
    df_grouped.columns = ['developer', 'Neutral', 'Negativo', 'Positivo']
    df_sorted = df_grouped.sort_values(by='Negativo', ascending=False).head(3)

    result = [{"Puesto {}".format(i+1): {"Desarrolladora": developer, "Puntuación Negativa": negative_points}} for i, (developer, negative_points) in enumerate(zip(df_sorted['developer'], df_sorted['Negativo']))]
    
    return JSONResponse(content=result)

@app.get('/sentiment_analysis')
def sentiment_analysis(developer: str):
    """
    Devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros
    de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.
    """
    df_filtered = developer_opinion[developer_opinion['developer'].notnull()]
    df_filtered['developer'] = df_filtered['developer'].astype(str)
    df_filtered = df_filtered[df_filtered['developer'] == developer]

    if df_filtered.empty:
        raise HTTPException(status_code=404, detail=f"Desarrolladora '{developer}' no encontrada")

    sentiment_counts = df_filtered['sentiment_analisis'].value_counts().to_dict()
    adjusted_sentiments = {2: "Positivo", 0: "Neutral", 1: "Negativo"}
    sentiment_counts = {adjusted_sentiments[key]: value for key, value in sentiment_counts.items()}

    result = {developer: sentiment_counts}
    return JSONResponse(content=result)

@app.get('/encontrar-juegos-similares')
def encontrar_juegos_similares(id_juego: int):
    try:
        juego_indice = modelo_final.index[modelo_final['id'] == id_juego].item()
    except ValueError:
        raise HTTPException(status_code=404, detail=f"El juego con el ID {id_juego} no existe en la base de datos.")

    juego_caracteristicas = modelo_final.iloc[juego_indice, 3:].values.reshape(1, -1)
    similitudes_render = cosine_similarity(modelo_final.iloc[:, 3:], juego_caracteristicas)
    indices_juegos_similares = similitudes_render.argsort(axis=0)[::-1][1:6].flatten()[1:]
    juegos_similares = modelo_final.iloc[indices_juegos_similares, 'title'].tolist()

    return JSONResponse(content=juegos_similares)
