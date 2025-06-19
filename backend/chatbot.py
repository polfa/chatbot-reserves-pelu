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

def extract_service_from_message(message, services):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    f"Ets un assistent que analitza el missatge de l'usuari i retorna el servei escollit de manera exacta.\n"
                    f"La llista de serveis vàlids és la següent: {services}.\n\n"
                    f"Instruccions:\n"
                    f"- Si el servei mencionat pel missatge és pràcticament idèntic (però no cal que sigui exacte en la redacció) a un dels de la llista, retorna aquest servei exactament com apareix a la llista.\n"
                    f"- No pots inventar-te serveis ni corregir errors si el resultat no és clarament identificable com un servei vàlid.\n"
                    f"- Si el missatge no conté cap servei clarament identificable de la llista, retorna exactament: ERROR.\n\n"
                    f"Exemples:\n"
                    f"- Si el missatge és 'Vull fer Keratrina', retorna: ERROR (Keratina no és a la llista).\n"
                    f"- Si el missatge és 'Em vull tallar el cabell', retorna: Tallat (si 'Tallat' és a la llista).\n"
                    f"- Si el missatge és 'Pintar ungles', retorna: ERROR.\n\n"
                    f"Només retorna un únic servei de la llista o la paraula ERROR. No afegeixis res més."
                ),
            },
            {"role": "user", "content": message},
        ]
    )
    return completion.choices[0].message.content.strip()

def extract_empleat_from_message(message, empleats):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    f"Ets un assistent que rep un missatge de l'usuari i ha de determinar si conté el nom d'un empleat vàlid.\n"
                    f"La llista d'empleats vàlids és: {empleats}.\n\n"
                    f"Instruccions:\n"
                    f"- Si el missatge conté clarament el nom d'un dels empleats de la llista, retorna exactament aquest nom (amb la mateixa ortografia, les majuscules es igual).\n"
                    f"- Si no hi ha cap coincidència clara amb un nom de la llista, retorna exactament: ERROR.\n"
                    f"- No inventis noms, no corregeixis, no assumeixis.\n"
                    f"- Només pots retornar un nom exacte de la llista o la paraula ERROR.\n\n"
                    f"Exemples:\n"
                    f"- Missatge: 'Vull reservar amb en Pol' → retorna: Pol (si és a la llista)\n"
                    f"- Missatge: 'Amb en Pauet' → retorna: ERROR (si Pauet no és a la llista)\n"
                    f"- Missatge: 'Qualsevol' o 'No tinc preferència' → retorna: ERROR\n\n"
                    f"Només has de respondre amb un dels noms exactes de la llista o amb la paraula ERROR. Res més."
                )
            },
            { "role": "user", "content": message }
        ]
    )
    c = completion.choices[0].message.content.strip()
    if c in empleats:
        return c
    else:
        return "ERROR"
    


