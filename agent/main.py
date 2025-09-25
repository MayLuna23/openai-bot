import os, json
import random
import requests
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurar modelo de OpenAI
llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

API_URL = "http://localhost:8000"


def query_api(keywords: list[str]):
    """Hace una búsqueda en la API local con múltiples palabras clave."""
    print(f"🔎 query_api: {keywords}")
    
    if keywords == []:
        # Si no hay keywords, traer todas las noticias (para luego tomar random)
        response = requests.get(f"{API_URL}/records")
        if response.status_code == 200:
            return response.json()
        return []
    
    response = requests.get(
        f"{API_URL}/records/search",
        params={"keyword": [kw.lower() for kw in keywords]}  # varias keywords
    )
    if response.status_code == 200:
        return response.json()
    return []


def agente_preguntar(texto: str):
    """Interpreta la pregunta, maneja ambigüedad y devuelve respuesta resumida."""
    
    if texto.strip() == "":
        return "Por favor, ingresa una pregunta o tema específico sobre noticias."
    
    prompt_news = ChatPromptTemplate.from_template("""
        Analiza el texto del usuario.

        Si el texto es malintencionado, ofensivo, violento, discriminatorio, ilegal o inmoral, responde SOLO con:
        {{
        "tipo": "MALINTENCIONADO"
        }}

        Si el texto es demasiado genérico, poco claro o ambiguo (ej: "dime noticias", "qué pasó hoy", "muéstrame algo"), responde SOLO con:
        {{
        "tipo": "AMBIGUA",
        "keywords": ["palabra1", "palabra2", ...]  # Si logras rescatar algo, pon al menos 1 palabra clave
        }}

        Si el texto es válido y específico, responde con:
        {{
        "tipo": "ESPECIFICA",
        "keywords": ["palabra1", "palabra2", ...]
        }}

        Reglas adicionales para el caso ESPECIFICA o AMBIGUA:
        - Las keywords deben estar en español (si el usuario escribe en inglés u otro idioma, tradúcelas).
        - Incluye entre 1 y 5 palabras relacionadas o sinónimos que ayuden a ampliar la búsqueda.
        - Mantén las keywords cortas y relevantes (ej: politics, sports, technology, Trump).

        Texto: "{texto}"
    """)
    
    chain = prompt_news | llm
    result = chain.invoke({"texto": texto})
    respuesta = result.content.strip()

    try:
        data = json.loads(respuesta)

        # Validación de malintencionado
        if data.get("tipo") == "MALINTENCIONADO":
            return "Lo siento, no puedo ayudarte o darte información interesante con el texto que me das, intenta con algo nuevo 😊"

        # Validación de ambigüedad
        if data.get("tipo") == "AMBIGUA":
            keywords = data.get("keywords", [])

            if keywords:
                resultados = query_api(keywords)
                if resultados:
                    resumen = "\n".join(
                        [f"- {r['title']} (Fuente: {r['source']})" for r in resultados[:3]]
                    )
                    return f"🤖 Encontré algunas noticias relacionadas con {', '.join(keywords)}:\n\n{resumen}\n\n👉 Si me das más detalles, puedo darte información más interesante."
            
            # Si no hay keywords útiles o no devolvió resultados → noticias random
            todos_resultados = query_api([])  # función que trae noticias sin filtro
            random_news = random.sample(todos_resultados, min(3, len(todos_resultados)))
            resumen_random = "\n".join(
                [f"- {r['title']} (Fuente: {r['source']})" for r in random_news]
            )
            return f"🤖 No encontré noticias con {keywords}, pero aquí tienes 3 noticias al azar:\n\n{resumen_random}\n\n👉 Dame más detalles y te mostraré noticias más relevantes."

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

        # Si el JSON no tiene un tipo esperado
        return "🤖 No entendí tu consulta, intenta con otro tema."

    except json.JSONDecodeError:
        # No era JSON → devolver mensaje genérico del LLM
        return {"message": respuesta}
    

if __name__ == "__main__":
    while True:
        pregunta = input("\nHazme una pregunta sobre noticias (o escribe 'salir'): ")
        if pregunta.lower() == "salir":
            break
        respuesta = agente_preguntar(pregunta)
        print("\n", respuesta)
