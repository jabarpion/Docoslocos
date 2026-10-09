from utils.chunker import dividir_en_chunks
from utils.buscador import buscar_chunks
from utils.lector_excel import leer_excel
from utils.consultor_excel import buscar_en_excel, dataframe_a_texto

import os
import streamlit as st
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        api_key = None

if not api_key:
    raise ValueError(
        "Falta GEMINI_API_KEY. Configúrala en .env "
        "o en los Secrets de Streamlit Cloud."
    )

cliente = genai.Client(api_key=api_key)


def preguntar_al_pdf(texto_pdf, pregunta, df_excel=None):

    # =========================
    # BUSCAR EN EL PDF
    # =========================

    chunks = dividir_en_chunks(texto_pdf)

    mejores_chunks = buscar_chunks(
        pregunta,
        chunks,
        top_k=5
    )

    contexto_pdf = "\n\n".join(mejores_chunks)


    # =========================
    # BUSCAR EN EL EXCEL
    # =========================

    contexto_excel = ""

    if df_excel is not None:

        resultados_excel = buscar_en_excel(
            df_excel,
            pregunta,
            max_resultados=10
        )

        contexto_excel = dataframe_a_texto(
            resultados_excel
        )


    # =========================
    # COMPROBAR SI HAY INFORMACIÓN
    # =========================

    if not contexto_pdf.strip() and (
        df_excel is None or not contexto_excel.strip()
    ):
        return "No encontré esa información en los documentos."


    print("Chunks totales:", len(chunks))
    print("Chunks recuperados:", len(mejores_chunks))

    print("\n--- CONTEXTO PDF ---")
    print(contexto_pdf[:1000])

    print("\n--- CONTEXTO EXCEL ---")
    print(contexto_excel[:1000])


    # =========================
    # CONSTRUIR CONTEXTO
    # =========================

    contexto = ""

    if contexto_pdf.strip():

        contexto += (
            "INFORMACIÓN DEL CÓDIGO DE CONDUCTA:\n\n"
            + contexto_pdf
            + "\n\n"
        )

    if contexto_excel.strip():

        contexto += (
            "INFORMACIÓN DE LA TABLA DE EMBALAJES Y ETIQUETAS:\n\n"
            + contexto_excel
        )


    if not contexto.strip():
        return "No encontré esa información en los documentos."


    # =========================
    # PROMPT
    # =========================

    prompt = f"""
Eres un asistente inteligente de FrutAlura.

Tu tarea es responder preguntas utilizando únicamente
la información contenida en el contexto entregado.

Reglas:

- No inventes información.
- No uses conocimiento externo.
- Utiliza únicamente la información del contexto.
- Si la respuesta está en la tabla de embalajes y etiquetas,
  utiliza esa información.
- Si la respuesta está en el Código de Conducta,
  utiliza esa información.
- Si la información necesaria no aparece en el contexto,
  responde exactamente:

"No encontré esa información en los documentos."

CONTEXTO:

{contexto}


PREGUNTA:

{pregunta}


RESPUESTA:
"""


    # =========================
    # CONSULTAR GEMINI
    # =========================

    try:

        respuesta = cliente.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return respuesta.text


    except Exception as e:

        return (
            "⚠️ El servicio de inteligencia artificial no está "
            "disponible en este momento. "
            "Intenta nuevamente en unos minutos.\n\n"
            f"Detalle técnico: {e}"
        )
