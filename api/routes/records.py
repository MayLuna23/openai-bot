from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from typing import List, Union, Optional
from sqlalchemy import text
from fastapi.security import APIKeyHeader
from db import get_db
from services.records import fetch_news_api, insert_articles_no_duplicates, search_news
from schemas.articles import Article 
from logs.logger_config import logger

router = APIRouter()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

@router.get(
    "/",
    summary="Endpoint raíz",
    description="Devuelve un mensaje de bienvenida con información básica sobre la API."
)
def home():
    logger.info("🌍 Endpoint raíz llamado")
    return {"message": "Bienvenido a la News API 🚀 Usa /docs para explorar los endpoints."}


@router.get(
    "/records",
    response_model=List[Article],
    summary="Listar artículos",
    description="Devuelve todos los artículos almacenados en la base de datos."
)
def list_records(db=Depends(get_db)):
    logger.info("📑 Listando todos los artículos de la DB")
    result = db.execute(text("SELECT * FROM news")).mappings().all()
    return list(result)


@router.get(
    "/records/search",
    response_model=List[Article],
    summary="Buscar artículos",
    description="""
    Busca artículos en la base de datos por palabra clave en **título o resumen**.
    
    - `keyword`: palabra(s) obligatorias (pueden ser varias).
    - `source`: fuente opcional.
    """,
)
def search_records(
    keyword: Union[str, List[str]] = Query(
        ..., 
        description="Palabra(s) clave en título o resumen",
        example="supervivientes"
    ),
    source: Optional[str] = Query(
        None,
        description="Nombre de la fuente",
        example="Www.abc.es"
    ),
    db=Depends(get_db)
):
    logger.info(f"🔍 Buscando artículos con keyword='{keyword}' y source='{source}'")
    results = search_news(db, keyword, source)
    logger.info(f"✅ {len(results)} resultados encontrados")
    return results


@router.get(
    "/records/update",
    response_model=dict,
    summary="Actualizar artículos desde NewsAPI",
    description="""
    Llama al servicio externo **NewsAPI** para obtener artículos recientes y los inserta
    en la base de datos si no existen.
    
    **Seguridad:** requiere el token válido:`supersecret` (se deja expuesto con fines de prueba técnica).
    """,
    responses={
        403: {"description": "Token inválido"},
        200: {
            "description": "Actualización exitosa",
            "content": {
                "application/json": {
                    "example": {"message": "Datos actualizados correctamente"}
                }
            },
        },
    }
)
def update_records(token: str, db=Depends(get_db)):
    if token != "supersecret":
        logger.error("❌ Token inválido en actualización de artículos")
        raise HTTPException(status_code=403, detail="Token inválido")
    logger.info("🔄 Actualizando artículos desde NewsAPI...")
    articles = fetch_news_api()
    logger.info(f"📥 {len(articles)} artículos obtenidos de NewsAPI")
    
    insert_articles_no_duplicates(articles)
    logger.info("✅ Base de datos actualizada con nuevos artículos")
    return {"message": "Datos actualizados correctamente"}


@router.get(
    "/records/{record_id}",
    response_model=Article,
    summary="Obtener artículo por ID",
    description="Devuelve un artículo específico a partir de su `record_id`.",
    responses={
        404: {"description": "Registro no encontrado"}
    }
)
def get_record(
    record_id: int = Path(
        ...,  
        description="ID del registro",
        example=1
    ), db=Depends(get_db)):
    logger.info(f"📄 Buscando artículo con ID={record_id}")
    result = db.execute(
        text("SELECT * FROM news WHERE id = :id"), {"id": record_id}
    ).mappings().first()
    if not result:
        logger.warning(f"⚠️ Artículo con ID={record_id} no encontrado")
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    logger.info(f"✅ Artículo con ID={record_id} encontrado")
    return result
