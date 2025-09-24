# Prueba Técnica --- Proyecto ETL · API · Agente de IA

**Resumen corto**\
Proyecto que extrae datos públicos (ETL), los normaliza y almacena en
una base local (SQLite), expone una API REST para consultar y actualizar
los registros, y proporciona un agente en Python que interpreta
preguntas en lenguaje natural y consulta la API.

------------------------------------------------------------------------

## Estructura del repositorio (resumen)

    /
    ├─ agent/
    │  └─ agent.py
    ├─ api/
    │  ├─ main.py
    │  └─ routes/
    │     └─ records.py
    ├─ services/
    │  ├─ db.py
    │  ├─ records.py
    │  └─ main.py (u otros scripts)
    ├─ etl/
    │  ├─ etl.py
    ├─ docs/
    │  └─ security.md
    ├─ news.db
    ├─ requirements.txt
    └─ README.md   <-- (este archivo)

------------------------------------------------------------------------

## Requisitos previos

-   Python 3.13

------------------------------------------------------------------------

## Instalación (local, con venv)

1.  Clona el repo (si no lo tienes local):

``` bash
git clone <tu-repo-url>
cd <tu-repo-folder>
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

4.  Variables de entorno (recomendado)

-   Si tu ETL usa una API (ej. NewsAPI) coloca la clave como variable de
    entorno. Ejemplo:

``` bash
export NEWS_API_KEY="tu_api_key_aqui"
# Windows PowerShell:
$env:NEWS_API_KEY="tu_api_key_aqui"
```

-   Si tu endpoint `/records/update` requiere un token, puedes usar la
    variable `UPDATE_TOKEN` o el valor literal que programaste (ej.
    `supersecret`). Ajusta según tu implementación.

------------------------------------------------------------------------

## Cómo ejecutar (local)

### 1) Ejecutar el ETL (obtener y cargar datos)

``` bash
# Ejecuta el script ETL que descarga y guarda en la BD local
python etl/etl.py
```

### 2) Levantar la API (FastAPI + uvicorn)

``` bash
uvicorn api.main:app --reload --port 8000
```

-   Accede a la docs automática: `http://127.0.0.1:8000/docs`

**Endpoints principales (ejemplos)**\
- `GET /records` --- listar registros.\
- `GET /records/{id}` --- obtener un registro por id.\
- `GET /records/search?q=palabra&filter=...` --- búsqueda por palabra
clave (ajusta parámetros según tu implementación).\
- `POST /records/update?token=<token>` --- forzar actualización desde
ETL (endpoint protegido).

### 3) Ejecutar el agente (Python)

``` bash
python agent/agent.py
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

