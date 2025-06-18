# backend/chatbot.py
import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from backend.validations import validate_iso_datetime, validate_name


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_bot_response(user_input):
    today = datetime.now().strftime("%Y-%m-%d")
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"Ets un assistent virtual per una perruqueria. Respon amb simpatia i de forma clara. Avui és {today}."},
            {"role": "user", "content": user_input},
        ]
    )
    m = completion.choices[0].message.content
    if validate_iso_datetime(m):
        return completion.choices[0].message.content
    else:
        return "ERROR"
    
def get_bot_introduction():
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"Ets un assistent virtual per una perruqueria. Escriuras el missatge a l'usuari similar a: ¡Hola! Soy tu asistente de reservas. ¿Cómo te llamas?. Pot ser en catala o castella pero ho pots dir de moltes formes diferents, sempre has de preguntar pel nom del client"},
        ]
    )
    return completion.choices[0].message.content

def extract_date_from_message(message):
    today = datetime.now().strftime("%Y-%m-%d")
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"Has d'analitzar el missatge de l'usuari i retornar la data de la reserva en format ISO 8601 (YYYY-MM-DDTHH:MM), sense text, nomes la data. Avui és {today}. Si diu 'dimarts que ve', calcula-ho correctament.Si no detectes cap data o es una data passada a avui retorna ERROR"},
            {"role": "user", "content": message},
        ]
    )
    m = completion.choices[0].message.content
    if validate_iso_datetime(m):
        return completion.choices[0].message.content
    else:
        return "ERROR"

def extract_name_from_message(message):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "Has d'analitzar el missatge de l'usuari i retornar únicament el nom propi "
                    "si l'usuari s'ha identificat, per exemple amb frases com 'Em dic Pol' o 'Sóc la Maria'. "
                    "Has de retornar només el nom, sense cap altra paraula, i en el mateix format que l'usuari "
                    "l'ha escrit (majúscules/minúscules). Si no es pot extreure cap nom, retorna 'UNKNOWN'."
                    "Si no detectes cap nom retorna ERROR"
                ),
            },
            {"role": "user", "content": message},
        ]
    )

    return completion.choices[0].message.content.strip()