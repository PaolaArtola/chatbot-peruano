# chatbot-peruano
# Chatbot de Comida Peruana

Chatbot con Streamlit que responde preguntas sobre gastronomía peruana
y permite preguntar por audio (transcripción con Whisper).

Se usó la biblioteca `openai` de Python conectada a GroqCloud, cuya API
es compatible con la de OpenAI.

- Chat: modelo openai/gpt-oss-20b
- Transcripción de audio: whisper-large-v3-turbo

## Cómo ejecutarlo
1. Instalar dependencias: pip install -r requirements.txt
2. Ejecutar: streamlit run app_groq.py
3. Ingresar tu propia API Key de Groq (gratis en console.groq.com)
   en la barra lateral.
