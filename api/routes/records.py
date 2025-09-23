# routes/news_routes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Union, Optional
from sqlalchemy import text

from db import get_db
from services.records import fetch_news_api, insert_articles_no_duplicates, search_news

router = APIRouter()

@router.get("/")
def home():
    return {"message": "Bienvenido a la News API 🚀 Usa /docs para explorar los endpoints."}

@router.get("/records")
def list_records(db=Depends(get_db)):
    result = db.execute(text("SELECT * FROM news")).mappings().all()
    # return len(result)
    return list(result)


@router.get("/records/search")
def search_records(
    keyword: Union[str, List[str]] = Query(..., description="Palabra(s) clave en título o resumen"),
    source: Optional[str] = None,
    db=Depends(get_db)
):
    return search_news(db, keyword, source)

@router.get("/records/{record_id}")
def get_record(record_id: int, db=Depends(get_db)):
    result = db.execute(text("SELECT * FROM news WHERE id = :id"), {"id": record_id}).mappings().first()
    if not result:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return result

@router.post("/records/update")
def update_records(token: str, db=Depends(get_db)):
    if token != "supersecret":
        raise HTTPException(status_code=403, detail="Token inválido")
    articles = fetch_news_api()
    print(len(articles), articles, " artículos obtenidos de NewsAPI")
    insert_articles_no_duplicates(articles)
    return {"message": "Datos actualizados correctamente"}
