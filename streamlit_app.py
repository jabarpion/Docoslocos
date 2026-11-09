import streamlit as st
from pathlib import Path

from utils.lector_pdf import leer_pdf
from utils.lector_excel import leer_excel
from utils.lector_docx import leer_docx
from utils.agente import preguntar_al_pdf


st.set_page_config(
    page_title="Docoslocos",
    page_icon="🤖"
)


@st.cache_data
def cargar_documentos():

    carpeta_documentos = Path(__file__).parent / "documentos"

    ruta_pdf = carpeta_documentos / "codigo_conducta_frutalura.pdf"
    ruta_excel = carpeta_documentos / "EMBALAJES ETIQUETAS KIWI.xlsx"
    ruta_docx = carpeta_documentos / "embalajes.docx"

    texto_pdf = leer_pdf(ruta_pdf)
    df_excel = leer_excel(ruta_excel)

    # Un problema en el OCR no debe impedir consultar PDF y Excel.
    try:
        texto_docx = leer_docx(ruta_docx)
    except Exception as error:
        texto_docx = ""
        st.warning(
            "No fue posible procesar el DOCX: "
            f"{type(error).__name__}"
        )

    return texto_pdf, df_excel, texto_docx


if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("🤖 Docoslocos")

st.write(
    "Haz preguntas sobre el Código de Conducta "
    "o sobre embalajes y etiquetas de kiwi."
)


for mensaje in st.session_state.messages:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])


pregunta = st.chat_input("Escribe tu pregunta...")


if pregunta:

    st.session_state.messages.append(
        {"role": "user", "content": pregunta}
    )

    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.spinner("Consultando documentos..."):

        texto_pdf, df_excel, texto_docx = cargar_documentos()

        respuesta = preguntar_al_pdf(
            texto_pdf,
            pregunta,
            df_excel,
            texto_docx
        )

    with st.chat_message("assistant"):
        st.markdown(respuesta)

    st.session_state.messages.append(
        {"role": "assistant", "content": respuesta}
    )
