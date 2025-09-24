import requests, os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
URL = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={NEWSAPI_KEY}"

resp = requests.get(URL)
data = resp.json()

engine = create_engine("sqlite:///./news.db")  # o tu conexión
with engine.begin() as conn:
    for article in data["articles"]:
        conn.execute(
            text("INSERT INTO news (title, summary, source) VALUES (:t, :d, :s)"),
            {"t": article["title"], "d": article["description"], "s": article["source"]["name"]}
        )

# Configura parámetros de la API
params = {
    "country": "us",    # noticias de USA
    "pageSize": 100,    # trae 100 noticias
    "apiKey": NEWSAPI_KEY
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
