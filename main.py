from fastapi import FastAPI
import pandas as pd
from fastapi import FastAPI, HTTPException
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from typing import List


app = FastAPI()



#Archivos para consumirse en la api
games=pd.read_parquet("DataSets/steam_games.parquet")
developer_opinion=pd.read_parquet("Funciones/developer_opinion.parquet")
user_items=pd.read_parquet("DataSets/user_items.parquet")
playtime=pd.read_parquet("Funciones/playtime.parquet")
modelo_final=pd.read_parquet("DatosML/ModeloFinal.parquet")



@app.get("/")
def read_root():
    return {"message": "Proyecto Individual"}

# Funciones de validación y optimización

def validate_genre(genre):
    """
    Valida si el género existe en el conjunto de datos.
    """
    genre_name = genre.capitalize()
    df_filtered = games[games['genres'].str.contains(genre, case=False, na=False)]
    if df_filtered.empty:
        raise HTTPException(status_code=404, detail=f"Género {genre_name} no encontrado")

def validate_year(year):
    """
    Valida si el año existe en el conjunto de datos.
    """
    if year not in developer_opinion['release_date'].unique():
        raise HTTPException(status_code=404, detail=f"Año {year} no encontrado")

# Primera función optimizada
@app.get("/")
def read_root():
    return {"message": "Proyecto Individual"}

# Funciones de validación y optimización

def validate_genre(genre):
    """
    Valida si el género existe en el conjunto de datos.
    """
    genre_name = genre.capitalize()
    df_filtered = games[games['genres'].str.contains(genre, case=False, na=False)]
    if df_filtered.empty:
        raise HTTPException(status_code=404, detail=f"Género {genre_name} no encontrado")

def validate_year(year):
    """
    Valida si el año existe en el conjunto de datos.
    """
    if year not in developer_opinion['release_date'].unique():
        raise HTTPException(status_code=404, detail=f"Año {year} no encontrado")

# Primera función optimizada
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