from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import init_db
from services.records import fetch_news_api, insert_articles_no_duplicates
from routes.records import router as news_router 
from logs.logger_config import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Iniciando aplicación FastAPI")
    init_db()
    logger.info("✅ Base de datos inicializada")
    articles = fetch_news_api()
    logger.info(f"📥 {len(articles)} artículos obtenidos de NewsAPI")
    insert_articles_no_duplicates(articles)
    logger.info("📑 Noticias iniciales cargadas en la base de datos")
    yield
    logger.info("🚪 Cerrando aplicación, limpiando recursos...")


app = FastAPI(
    title="News API",
    description="""
    API para gestionar artículos de noticias extraídos de **NewsAPI**.

    ### Funcionalidades principales:
    - 📥 **ETL automático**: extrae, transforma y carga noticias en SQLite.
    - 📑 **Consulta de artículos**: obtén artículos ya procesados.
    - 🔄 **Actualización de registros**: fuerza la recarga de noticias.

    ---
    """,
    
    lifespan=lifespan,
)


# Registrar el router con un tag
app.include_router(news_router, tags=["Records"])
