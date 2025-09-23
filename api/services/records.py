# services/news_service.py
from sqlalchemy import text
import requests
from db import engine

API_KEY = "00ccf55498574b80ae2cd0e2f24af004"
NEWS_URL = f"https://newsapi.org/v2/everything?q=all&language=es&apiKey=00ccf55498574b80ae2cd0e2f24af004"
# NEWS_URL = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={API_KEY}"

def fetch_news_api():
    try:
        # pageSize máximo permitido es 100
        params = {
            "pageSize": 100,
            "page": 1,  # primera página
        }
        resp = requests.get(NEWS_URL, params=params)
        resp.raise_for_status()
        data = resp.json()
        print(len(data["articles"])," artículos obtenidos de NewsAPI")
        return resp.json().get("articles", [])
    except Exception as e:
        print("Error al consultar NewsAPI:", e)
        return []

def insert_articles_no_duplicates(articles):
    with engine.begin() as conn:
        for article in articles:
            title = article.get("title")
            summary = article.get("description")
            source = article.get("source", {}).get("name")
            if not title:
                continue
            conn.execute(
                text("INSERT OR IGNORE INTO news (title, summary, source) VALUES (:t, :s, :src)"),
                {"t": title, "s": summary, "src": source}
            )

def search_news(db, keywords, source=None):
    # keywords ya es una lista
    if not keywords:
        keywords = []

    conditions = []
    params = {}
    for i, kw in enumerate(keywords):
        conditions.append(f"(title LIKE :kw{i} OR summary LIKE :kw{i})")
        params[f"kw{i}"] = f"%{kw}%"

    query = "SELECT * FROM news"
    if conditions:
        query += " WHERE (" + " OR ".join(conditions) + ")"
        if source:
            query += " AND source = :src"
            params["src"] = source
    elif source:
        query += " WHERE source = :src"
        params["src"] = source

    result = db.execute(text(query), params).mappings().all()
    return list(result)


