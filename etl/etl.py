import requests
import pandas as pd
from sqlalchemy import create_engine

API_KEY = "00ccf55498574b80ae2cd0e2f24af004"
URL = "https://newsapi.org/v2/top-headlines"

# Configura parámetros de la API
params = {
    "country": "us",    # noticias de USA
    "pageSize": 100,    # trae 100 noticias
    "apiKey": API_KEY
}

def fetch_data():
    response = requests.get(URL, params=params)
    data = response.json()
    return data["articles"]

def transform_data(articles):
    rows = []
    for idx, art in enumerate(articles, start=1):
        rows.append({
            "id": idx,
            "title": art.get("title"),
            "author": art.get("author"),
            "source": art.get("source", {}).get("name"),
            "published_at": art.get("publishedAt"),
            "url": art.get("url"),
            "summary": art.get("description")
        })
    return pd.DataFrame(rows)

def load_data(df):
    engine = create_engine("sqlite:///../news.db")  # guarda en la raíz
    df.to_sql("news", engine, if_exists="replace", index=False)
    print("✅ Datos guardados en news.db")

if __name__ == "__main__":
    articles = fetch_data()
    df = transform_data(articles)
    load_data(df)
    print(df.head())  # muestra los primeros 5
