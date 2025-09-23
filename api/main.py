from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import init_db
from services.records import fetch_news_api, insert_articles_no_duplicates
from routes.records import router as news_router  # <--- importar router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    articles = fetch_news_api()
    insert_articles_no_duplicates(articles)
    print("✅ DB inicializada y noticias cargadas")
    yield
    print("🚪 App cerrando, limpiando recursos...")

app = FastAPI(title="News API", lifespan=lifespan)

# Registrar el router
app.include_router(news_router)
