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
