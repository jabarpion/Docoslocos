from utils.chunker import dividir_en_chunks
from utils.buscador import buscar_chunks
from utils.lector_excel import leer_excel
from utils.consultor_excel import buscar_en_excel, dataframe_a_texto

import os
import streamlit as st
from google import genai

api_keys = []

api_keys = [key.strip() for key in api_keys if key and key.strip()]

# Eliminar claves duplicadas, conservando el orden
api_keys = list(dict.fromkeys(api_keys))

if not api_keys:
    raise ValueError(
        "No hay API Keys configuradas. "
        "Revisa GEMINI_API_KEYS en Streamlit Secrets."
    )

# 1. Leer varias claves desde variables de entorno
env_keys = os.getenv("GEMINI_API_KEYS", "").strip()

if env_keys:
    api_keys = [
        key.strip()
        for key in env_keys.split(",")
        if key.strip()
    ]

# 2. Compatibilidad con una sola clave en el entorno
if not api_keys and os.getenv("GEMINI_API_KEY"):
    api_keys = [os.getenv("GEMINI_API_KEY")]

# 3. Leer los Secrets de Streamlit
if not api_keys:
    try:
        secret_keys = st.secrets.get("GEMINI_API_KEYS", [])

        if isinstance(secret_keys, str):
            api_keys = [
                key.strip()
                for key in secret_keys.split(",")
                if key.strip()
            ]
        else:
            api_keys = list(secret_keys)

        if not api_keys:
            single_key = st.secrets.get("GEMINI_API_KEY")
            if single_key:
                api_keys = [single_key]

    except Exception:
        api_keys = []

# 4. Comprobar la configuración
api_keys = [key for key in api_keys if key]

if not api_keys:
    raise ValueError(
        "No se encontraron API Keys. Configura GEMINI_API_KEYS "
        "o GEMINI_API_KEY en los Secrets de Streamlit."
    )

# Inicializar Gemini con la primera clave
cliente = genai.Client(api_key=api_keys[0])


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
    # CONSULTAR GEMINI CON ROTACIÓN DE CLAVES
    # =========================

    errores = []

    for indice, api_key in enumerate(api_keys):
        try:
            cliente = genai.Client(api_key=api_key)

            respuesta = cliente.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            if respuesta.text:
                return respuesta.text

            return "El modelo no devolvió una respuesta de texto."

        except Exception as e:
            status = (
                getattr(e, "code", None)
                or getattr(e, "status_code", None)
            )

            mensaje = str(e).lower()

            # Errores en los que tiene sentido probar otra clave
            reintentable = (
                status in (401, 403, 429, 500, 502, 503, 504)
                or any(
                    termino in mensaje
                    for termino in (
                        "resource_exhausted",
                        "quota exceeded",
                        "rate limit",
                        "api key not valid",
                        "invalid api key",
                    )
                )
            )

            # Guardar solo información técnica del error,
            # nunca la clave utilizada
            errores.append(
                f"Clave {indice + 1}: "
                f"{type(e).__name__}, código={status}"
            )

            if not reintentable:
                print("Error de Gemini:", errores[-1])
                return (
                    "No se pudo completar la consulta. "
                    "Revisa los registros de la aplicación."
                )

            print("Se intentará otra clave:", errores[-1])

    print("Se agotaron las API Keys configuradas.")

    return (
        "⚠️ No se pudo obtener una respuesta de Gemini "
        "con las claves configuradas. Comprueba las cuotas, "
        "los permisos y la validez de las claves."
    )
