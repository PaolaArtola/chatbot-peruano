import os

import streamlit as st
from openai import OpenAI

# ---------------------------------------------------------------
# Configuración de la página
# ---------------------------------------------------------------
st.set_page_config(page_title="Chatbot de Comida Peruana", page_icon="🍽️")
st.title("🍽️ Chatbot de Comida Peruana")
st.caption("Pregúntame sobre ceviche, ají de gallina, pachamanca y mucho más.")

# ---------------------------------------------------------------
# Barra lateral: API key y transcripción de audio (Parte 2)
# ---------------------------------------------------------------
api_key = st.sidebar.text_input(
    "Groq API Key (gratis)",
    type="password",
    value=os.getenv("GROQ_API_KEY", ""),
)

if not api_key:
    st.info("Ingresa tu API Key de Groq en la barra lateral para comenzar.")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

MODELO = "openai/gpt-oss-20b"

SYSTEM_PROMPT = (
    "Eres un experto en gastronomía peruana. Respondes en español, de forma "
    "clara y amable, sobre platos típicos, ingredientes, recetas, historia y "
    "regiones del Perú. Si la pregunta no trata sobre comida peruana, indica "
    "amablemente que solo puedes conversar sobre ese tema."
)

# ---------------------------------------------------------------
# Estado de la sesión: aquí se guarda el historial de la conversación
# ---------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]


def responder(pregunta: str):
    """Envía la pregunta al modelo con todo el historial y muestra la respuesta."""
    st.session_state.messages.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=MODELO,
            messages=st.session_state.messages,
            stream=True,
        )
        respuesta = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": respuesta})


# ---------------------------------------------------------------
# Parte 2: subir audio y transcribirlo con Whisper
# ---------------------------------------------------------------
st.sidebar.divider()
st.sidebar.subheader("🎤 Preguntar con audio")
audio = st.sidebar.file_uploader(
    "Sube un audio con tu pregunta",
    type=["mp3", "wav", "m4a", "mp4", "mpeg", "mpga", "webm"],
)

pregunta_por_audio = None
if audio is not None and st.sidebar.button("Transcribir y preguntar"):
    with st.spinner("Transcribiendo audio..."):
        transcripcion = client.audio.transcriptions.create(
            model="whisper-large-v3-turbo",
            file=(audio.name, audio.getvalue()),
            language="es",
        )
    pregunta_por_audio = transcripcion.text
    st.sidebar.success("Transcripción:")
    st.sidebar.write(pregunta_por_audio)

# ---------------------------------------------------------------
# Mostrar el historial (sin el mensaje "system")
# ---------------------------------------------------------------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ---------------------------------------------------------------
# Entrada de texto y respuesta
# ---------------------------------------------------------------
if pregunta_por_audio:
    responder(pregunta_por_audio)

if prompt := st.chat_input("Escribe tu pregunta sobre comida peruana..."):
    responder(prompt)
