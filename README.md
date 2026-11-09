# 🤖 Agente Inteligente Docoslocos copia y mejora de FrutAlura.

Presento mi Agente Inteligente pensado en una solución tecnológica a las múltiples preguntas que deben responder en Recursos Humanos y/o los embalajes de producción de una empresa frutícola.

Agente de Inteligencia Artificial desarrollado como solución al **Challenge Alura Agente**. La aplicación responde preguntas sobre el **Código de Conducta y Ética Empresarial de FrutAlura**, utilizando como única fuente de información un documento PDF almacenado localmente.

El proyecto implementa un flujo **RAG (Retrieval-Augmented Generation)** sencillo: antes de enviar una consulta al modelo de lenguaje, recupera únicamente los fragmentos más relevantes del documento, reduciendo el contexto enviado y mejorando la precisión de las respuestas.

---

# 🚀 Aplicación en línea

La aplicación está desplegada en **Streamlit Community Cloud**.

**URL:** https://frutalura-t5sqymuhxa9xkh3yljkbrd.streamlit.app/

---

---

# Características

- Lectura automática del documento PDF.
- Lectura de documento Excel.
- División del documento en fragmentos (chunks).
- Recuperación de los fragmentos más relevantes según la pregunta.
- Generación de respuestas mediante Google Gemini.
- Interfaz web desarrollada con Streamlit.
- El agente responde únicamente utilizando la información contenida en el documento.

---

# Arquitectura de la solución

El proyecto sigue un flujo RAG básico compuesto por cuatro etapas:

```
Pregunta del usuario
        │
        ▼
Lectura del PDF
        │
        ▼
División en Chunks
        │
        ▼
Buscador de Chunks
        │
        ▼
Construcción del Contexto
        │
        ▼
Google Gemini
        │
        ▼
Respuesta al usuario
```

### Componentes

**lector_pdf.py**

Lee el documento PDF y extrae su contenido en texto.

**chunker.py**

Divide el documento en fragmentos con solapamiento para conservar el contexto entre secciones.

**buscador.py**

Busca los fragmentos más relacionados con la pregunta mediante coincidencia de palabras clave, descartando palabras vacías (StopWords).

**agente.py**

Construye el contexto con los fragmentos recuperados, genera el prompt y consulta la API de Google Gemini.

**streamlit_app.py**

Interfaz web que permite al usuario realizar preguntas y visualizar las respuestas.

---

# Estructura del proyecto

```
FrutAlura/
│
├── documentos/
│   └── codigo_conducta_frutalura.pdf
│
├── utils/
│   ├── agente.py
│   ├── buscador.py
│   ├── chunker.py
│   └── lector_pdf.py
│
├── streamlit_app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Tecnologías utilizadas

- Python 3
- Streamlit
- Google Gemini API
- Google GenAI SDK
- PyPDF
- Python Dotenv
- Git
- GitHub

---

# Funcionamiento

1. El sistema lee el documento PDF o Excel.
2. El documento se divide en fragmentos.
3. El buscador recupera los fragmentos más relacionados con la pregunta.
4. Se construye un contexto con los mejores fragmentos.
5. El contexto se envía a Google Gemini.
6. Gemini genera una respuesta utilizando únicamente la información recuperada.

---

# Instalación

Clonar el repositorio:

```bash
git clone https://github.com/jabarpion/FrutAlura.git
```

Entrar al proyecto:

```bash
cd FrutAlura
```

Crear un entorno virtual:

```bash
python -m venv venv
```

Activar el entorno virtual:

**Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Crear un archivo `.env` con la clave de Google Gemini:

```text
GEMINI_API_KEY=TU_API_KEY
```

Ejecutar la aplicación:

```bash
streamlit run streamlit_app.py
```

---

# Despliegue

La aplicación fue publicada utilizando **Streamlit Community Cloud**.

Una vez desplegada, puede accederse mediante la URL pública correspondiente al proyecto.

---

# Documento utilizado

Fuente de información:

- Código de Conducta y Ética Empresarial de FrutAlura (PDF)
- EMBALAJES ETIQUETAS KIWI (Excel)

El agente utiliza exclusivamente este documento para responder preguntas.

---

# Ejemplos de preguntas

- ¿Qué es el Código de Conducta?
- ¿Cuáles son los valores de FrutAlura?
- ¿Para quién es el Código de Conducta?
- ¿Qué responsabilidades tienen los colaboradores?
- ¿Qué establece el Código respecto a la integridad?
- ¿Qué normas existen sobre conflictos de interés?
- ¿Cómo deben protegerse los activos de la empresa?
- ¿Qué indica el documento sobre confidencialidad?
- Bolsa embalaje 10C
- Embalaje 9CS
- Embalaje hayward A1E

---

# Ejemplos de respuestas

**Pregunta**

> ¿Qué es el Código de Conducta?

**Respuesta**

> El Código de Conducta y Ética Empresarial representa el compromiso de FrutAlura de desarrollar todas sus actividades con integridad, honestidad y altos estándares éticos, orientando el comportamiento esperado de todos sus colaboradores.

---

**Pregunta**

> ¿Cuáles son los valores de FrutAlura?

**Respuesta**

> El documento describe los valores corporativos que orientan la conducta de los colaboradores y sirven como base para la toma de decisiones dentro de la organización.

---

**Pregunta**

> soreli T6C

**Respuesta**

> Aquí tienes la información para SORELI T6C:

    ESPECIE: SORELI
    COLOR: EF
    EMBALAJE: T6C
    CATEGORÍA: 1
    PLU: NO
    DESTINO: INGLATERRA
    CLIENTE: DPSL (TESCO)
    ENVASE: CAJA TESCO SPECIAL
    BOLSA: CARGO 938
    PESO: 6600


---

# Consideraciones

- El agente responde únicamente utilizando la información recuperada desde el documento.
- No utiliza conocimiento externo para generar respuestas.
- Si la información no está presente en el documento, informa explícitamente que no fue encontrada.

---

# Autor

**David Urbina Figueroa**

GitHub: https://github.com/jabarpion

Proyecto desarrollado como entrega del **Challenge Alura Agente**.


## Capturas de pantalla

1-1
1-2
2-1...
