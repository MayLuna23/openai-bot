# Prueba Técnica --- Proyecto ETL · API · Agente de IA

# API KEY OPEN AI Para prueba tecnica
Para correr el agente de Python debes pegar en el .env la OPENAI_API_KEY que se envia por correo
no se adjunta en el codigo para evitar que se invalide

**Resumen corto**\
Proyecto que extrae datos públicos (ETL), los normaliza y almacena en
una base local (SQLite), expone una API REST para consultar y actualizar
los registros, y proporciona un agente en Python que interpreta
preguntas en lenguaje natural y consulta la API.

------------------------------------------------------------------------

## Estructura del repositorio (resumen)

```bash
/
├── agent/
│   └── main.py
├── api/
│   ├── logs/
│   │   └── logger_config.py
│   ├── routes/
│   │   └── records.py
│   ├── schemas/
│   │   └── articles.py
│   ├── services/
│   │   └── records.py
│   ├── main.py
│   ├── db.py
│   └── news.db
├── docs/
│   └── security.md
├── etl/
│   └── etl.py
├── venv/
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

------------------------------------------------------------------------

## Requisitos previos

-   Python 3.13

------------------------------------------------------------------------

## Instalación (local, con venv)

1.  Clona el repo:

``` bash
git clone `https://github.com/MayLuna23/openai-bot.git`
cd openai-bot
```

2.  Crea y activa un entorno virtual:

``` bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\activate
```

3.  Instala dependencias:

``` bash
pip install -r requirements.txt
```

4.  Variables de entorno (.env)

  - NEWSAPI_KEY
  - OPENAI_API_KEY

-   El endpoint `/records/update` requiere un token simple `/records/update?token=supersecret`

------------------------------------------------------------------------

## Cómo ejecutar (local)

### 1) Levantar la API (FastAPI + uvicorn) y ETL

-   Al levantar la API automaticamente corre el proceso ETL y guardamos en la base de datos SQLite:

``` bash
cd api
uvicorn main:app --reload --port 8000
```

-   Accede a la docs automática: `http://localhost:8000/docs`

**Endpoints principales (ejemplos)**\
- `GET /records` --- listar registros.\
- `GET /records/{id}` --- obtener un registro por id.
- `GET /records/search?keyword=palabra` --- búsqueda por palabra clave.\
- `GET /records/update?token=supersecret` --- forzar actualización desde ETL (endpoint protegido).

### 2) Ejecutar el agente (Python)

``` bash
python agent/main.py
```

------------------------------------------------------------------------

## Seguridad (resumen) --- ver `docs/security.md`

-   El repo incluye `docs/security.md` con el análisis de riesgos y
    medidas recomendadas.

------------------------------------------------------------------------

## Datos locales

-   Archivo de ejemplo de DB: `news.db` (SQLite).\
-   Si quieres borrar datos y recargar:

``` bash
rm news.db
python etl/etl.py
```

-   Sin embargo, al correr la API por primera vez la base de datos se crea y se le inserta información.

