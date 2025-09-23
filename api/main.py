from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import List, Optional, Union, List

# Configuración de la base de datos
DATABASE_URL = "sqlite:///../news.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

app = FastAPI(title="News API", version="1.0")

# Dependencia para obtener la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ Endpoints ------------------ #

# Endpoint raíz (home)
@app.get("/")
def home():
    return {"message": "Bienvenido a la News API 🚀 Usa /docs para explorar los endpoints."}


# Listar todos los registros
@app.get("/records")
def list_records(db=Depends(get_db)):
    result = db.execute(text("SELECT * FROM news")).mappings().all()
    return list(result)

# Buscar con palabra clave y filtros
@app.get("/records/search")
def search_records(
    keyword: Union[str, List[str]] = Query(..., description="Palabra(s) clave en título o resumen"),
    source: Optional[str] = None,
    db=Depends(get_db)
):
    print(f"🔍 search_records called with keyword={keyword}, source={source}")
    # Normalizamos a lista
    if isinstance(keyword, str):
        keywords = [kw.strip() for kw in keyword.split(",")]
    else:
        keywords = keyword
        

    conditions = []
    params = {}
    for i, kw in enumerate(keywords):
        conditions.append(f"(title LIKE :kw{i} OR summary LIKE :kw{i})")
        params[f"kw{i}"] = f"%{kw}%"

    query = "SELECT * FROM news WHERE " + " OR ".join(conditions)

    if source:
        query += " AND source = :src"
        params["src"] = source

    result = db.execute(text(query), params).mappings().all()
    return list(result)


# Obtener un registro por ID
@app.get("/records/{record_id}")
def get_record(record_id: int, db=Depends(get_db)):
    result = db.execute(text("SELECT * FROM news WHERE id = :id"), {"id": record_id}).mappings().first()
    if not result:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return result



# # Buscar con palabra clave y filtros
# @app.get("/records/search")
# def search_records(
#     keyword: Union[str, List[str]] = Query(..., description="Palabra(s) clave en título o resumen"),
#     source: Optional[str] = None,
#     db=Depends(get_db)
# ):
#     print(f"🔍 search_records called with keyword={keyword}, source={source}")
#     # Normalizamos a lista
#     if isinstance(keyword, str):
#         keywords = [kw.strip() for kw in keyword.split(",")]
#     else:
#         keywords = keyword

#     conditions = []
#     params = {}
#     for i, kw in enumerate(keywords):
#         conditions.append(f"(title LIKE :kw{i} OR summary LIKE :kw{i})")
#         params[f"kw{i}"] = f"%{kw}%"

#     query = "SELECT * FROM news WHERE " + " OR ".join(conditions)

#     if source:
#         query += " AND source = :src"
#         params["src"] = source

#     result = db.execute(text(query), params).mappings().all()
#     return list(result)

# @app.get("/records/search")
# def search_records(
#     keyword: str = Query(..., description="Palabra clave en título o resumen"),
#     source: Optional[str] = None,
#     db=Depends(get_db)
# ):
#     query = "SELECT * FROM news WHERE (title LIKE :kw OR summary LIKE :kw)"
#     params = {"kw": f"%{keyword}%"}
#     if source:
#         query += " AND source = :src"
#         params["src"] = source
#     result = db.execute(text(query), params).mappings().all()
#     return list(result)

# Actualizar datos vía ETL (protegido con token)
@app.post("/records/update")
def update_records(token: str, db=Depends(get_db)):
    if token != "supersecret":
        raise HTTPException(status_code=403, detail="Token inválido")

    # Importar y ejecutar el ETL
    import sys
    sys.path.append("../etl")
    import etl
    articles = etl.fetch_data()
    df = etl.transform_data(articles)
    etl.load_data(df)

    return {"message": "Datos actualizados correctamente"}
