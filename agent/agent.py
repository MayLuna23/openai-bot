import os, json
import requests
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Configurar modelo de OpenAI
llm = ChatOpenAI(model="gpt-4o-mini")

API_URL = "http://localhost:8000"  # URL de tu API local


def query_api(keywords: list[str]):
    """Hace una búsqueda en la API local con múltiples palabras clave."""
    print(f"🔎 query_api: {keywords}")
    response = requests.get(
        f"{API_URL}/records/search",
        params={"keyword": [kw.lower() for kw in keywords]}  # varias keywords
    )
    if response.status_code == 200:
        return response.json()
    return []

def agente_preguntar(texto: str):
    """Interpreta la pregunta, maneja ambigüedad y devuelve respuesta resumida."""
    prompt_news = ChatPromptTemplate.from_template("""
        Analiza el texto del usuario.

        1. Si el texto es muy genérico (ej: "dime noticias", "qué pasó hoy", "muéstrame algo"), responde SOLO con:
        Tu pregunta es muy general. ¿De qué tema específico quieres noticias? Ejemplos: política, deportes, tecnología.


        2. Si el texto es suficientemente claro identifica la palabra clave principal para buscar en una API de noticias que está en inglés., responde en JSON con el formato:
        {{
        "tipo": "ESPECIFICA",
        "keywords": ["palabra1", "palabra2", ...]
        }}
        
        Reglas adicionales:
        - Las keywords deben estar en inglés (si el usuario escribe en español, tradúcelas).
        - Incluye entre 1 y 5 palabras relacionadas o sinónimos que ayuden a ampliar la búsqueda.
        - Evita palabras genéricas como "news", "latest", "noticias".
        - Mantén las keywords cortas y relevantes (ej: politics, sports, technology, Trump).


        Texto: "{texto}"
        """)
    
    chain = prompt_news | llm
    result = chain.invoke({"texto": texto})
    respuesta = result.content.strip()

    try:
        data = json.loads(respuesta)
        if data.get("tipo") == "ESPECIFICA":
            keywords = data["keywords"]
            resultados = query_api(keywords)

            if not resultados:
                return f"🤖 No encontré noticias relacionadas con {keywords}."

            # Tomar los 5 primeros resultados y resumirlos
            resumen = "\n".join(
                [f"- {r['title']} (Fuente: {r['source']})" for r in resultados[:5]]
            )
            return f"🤖 🔎 Encontré noticias sobre {', '.join(keywords)}:\n\n{resumen}"

    except json.JSONDecodeError:
        # No era JSON → devolver mensaje genérico del LLM
        return {"message": respuesta}

    return respuesta



if __name__ == "__main__":
    while True:
        pregunta = input("\nHazme una pregunta sobre noticias (o escribe 'salir'): ")
        if pregunta.lower() == "salir":
            break
        respuesta = agente_preguntar(pregunta)
        print("\n", respuesta)
        
        
        
        
        
        
        
        
        
        
        
        
# # Palabras demasiado genéricas
# genericas = ["noticias", "información", "cosas", "todo", "dame", "muéstrame"]

# # Si la pregunta es puramente genérica, pedimos aclaración
# if all(word.lower() in genericas for word in pregunta.lower().split()):
#     return "🤖 Tu pregunta es muy general. ¿De qué tema específico quieres noticias? Ejemplos: política, deportes, tecnología."

# Pedimos a OpenAI la palabra clave principal
#     prompt_keyword = ChatPromptTemplate.from_template(
#     "El usuario pregunta: {pregunta}. "
#     "Identifica la palabra clave principal para buscar en una API de noticias que está en inglés. "
#     "Responde SOLO con una palabra o frase corta en inglés, sin traducciones ni explicaciones."
# )


# chain_keyword = prompt_keyword | llm
# keyword = chain_keyword.invoke({"pregunta": pregunta}).content.strip()
# print("keyword", keyword)
# # Consultamos la API con búsqueda más flexible
# resultados = query_api(keyword)

# if not resultados:
#     return f"🤖 No encontré noticias relacionadas con '{keyword}'."

# # Tomamos los 5 primeros y resumimos
# resumen = "\n".join(
#     [f"- {r['title']} (Fuente: {r['source']})" for r in resultados[:5]]
# )

# return f"🤖 🔎 Busqué con la palabra clave '{keyword}'. Aquí tienes las 5 noticias más relevantes:\n\n{resumen}"

