# backend/chatbot.py

import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from backend.validations import validate_iso_datetime, validate_name

# Carga variables de entorno (.env)
load_dotenv()

# Cliente Groq, compatible con OpenAI
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "compound-beta"  # Modelo potente y gratuito

# ======================
# 1. Mensaje general del bot
# ======================
def get_bot_response(user_input):
    today = datetime.now().strftime("%Y-%m-%d")
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": f"Ets un assistent virtual per una perruqueria. Respon amb simpatia i de forma clara. Avui és {today}."},
            {"role": "user", "content": user_input},
        ]
    )
    m = completion.choices[0].message.content
    if validate_iso_datetime(m):
        return m
    else:
        return "ERROR"

# ======================
# 2. Introducció inicial
# ======================
def get_bot_introduction():
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": (
                    "Ets un assistent virtual per una perruqueria. Escriuràs un missatge per saludar l'usuari "
                    "i preguntar-li com es diu. Pots fer-ho en català o castellà, amb estil simpàtic pero ha de ser curtet. "
                    "Exemples: 'Hola! Com et dius?' o '¡Hola! ¿Cómo te llamas?'."
                )
            }
        ]
    )
    return completion.choices[0].message.content

# ======================
# 3. Extracció de data
# ======================
def extract_date_from_message(message):
    today = datetime.now().strftime("%Y-%m-%d")
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Analitza el missatge de l'usuari i retorna només la data de la reserva en format ISO 8601 "
                    "(YYYY-MM-DDTHH:MM), sense cap text addicional. Avui és " + today +
                    ". Si diu 'dimarts que ve', interpreta-ho bé. Si la data és passada o no hi ha cap data clara, retorna ERROR."
                )
            },
            {"role": "user", "content": message},
        ]
    )
    m = completion.choices[0].message.content.strip()
    return m if validate_iso_datetime(m) else "ERROR"

# ======================
# 4. Extracció del nom
# ======================
def extract_name_from_message(message):
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Analitza el missatge de l'usuari i retorna només el nom propi si s'ha identificat. "
                    "Exemples: 'Em dic Pol', 'Sóc la Maria'. Retorna només el nom tal com l'ha escrit l'usuari, "
                    "sense cap altra paraula. Si no detectes cap nom, retorna ERROR."
                )
            },
            {"role": "user", "content": message},
        ]
    )
    m = completion.choices[0].message.content.strip()
    return m if m and m.upper() != "UNKNOWN" else "ERROR"
