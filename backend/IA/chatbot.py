import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from backend.IA.validations import validate_iso_datetime, validate_name

load_dotenv()

class ChatbotAPI:
    def __init__(self, client_name="openai"):
        self.client = None
        self.set_client(client_name)

    def set_client(self, client_name):
        if client_name == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = "gpt-4o"
        elif client_name == "groq":
            self.client = OpenAI(
                api_key=os.getenv("GROQ_API_KEY"),
                base_url="https://api.groq.com/openai/v1"
            )
            self.model = "compound-beta"
        else:
            raise ValueError("Invalid client name")

    def get_bot_response(self, user_input):
        today = datetime.now().strftime("%Y-%m-%d")
        completion = self.client.chat.completions.create(
            model = self.model,
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
        
    def get_bot_introduction(self):
        completion = self.client.chat.completions.create(
            model = self.model,
            messages=[
                {"role": "system", "content": f"Ets un assistent virtual per una perruqueria. Escriuras el missatge a l'usuari similar a: ¡Hola! Soy tu asistente de reservas. ¿Cómo te llamas?. Pot ser en catala o castella pero ho pots dir de moltes formes diferents, sempre has de preguntar pel nom del client"},
            ]
        )
        return completion.choices[0].message.content

    def extract_date_from_message(self, message):
        today = datetime.now().strftime("%Y-%m-%d")
        completion = self.client.chat.completions.create(
            model = self.model,
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

    def extract_name_from_message(self, message):
        completion = self.client.chat.completions.create(
            model = self.model,
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

    def extract_service_from_message(self, message, services):
        completion = self.client.chat.completions.create(
            model = self.model,
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
                        f"SI ES UNA CONSULTA DEL SERVEI RETORNA: CONSULTA, ja que pot ser que estigui demanant info pero no escollint"
                    ),
                },
                {"role": "user", "content": message},
            ]
        )
        return completion.choices[0].message.content.strip()

    def extract_empleat_from_message(self, message, empleats):
        completion = self.client.chat.completions.create(
            model = self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"Ets un assistent que rep un missatge i ha de dir si conté el nom d’un empleat vàlid.\n"
                        f"Llista d’empleats: {empleats}.\n\n"
                        f"Respon només amb:\n"
                        f"- Un nom exacte de la llista (sense tenir en compte majuscules).\n"
                        f"- 'Qualsevol' si ho demana explícitament.\n"
                        f"- 'CONSULTA' si pregunta per info sobre empleats. Exemple: Qui es el Marc? o Que fa l'Andrea?\n"
                        f"- 'ERROR' si no coincideix cap nom clarament.\n\n"
                        f"No corregeixis, no inventis, no suposis. Respon només amb un valor exacte."
                    )
                },
                { "role": "user", "content": message }
            ]
        )
        c = completion.choices[0].message.content.strip()
        if c in empleats or c in ["ERROR", "CONSULTA", "Qualsevol"]:
            return c
        else:
            return "ERROR"



    def get_services_info(self, message, services):
        # Preparamos la lista de servicios para mostrar en la instrucción
        serveis_info = "\n".join([f"- {s.nom}: {s.duracio} min, {s.preu} euros" for s in services])

        prompt = (
            "Ets un assistent que rep un missatge on l'usuari pregunta per un servei de perruqueria (ex: tinte, tall, etc.) i/o "
            "vol saber la durada i preu d'aquest servei.\n"
            f"La llista de serveis disponibles és:\n{serveis_info}\n\n"
            "Instruccions:\n"
            "- Si el missatge conté clarament el nom d'un servei, respon només amb una frase clara i concreta amb la durada i preu, "
            "per exemple: 'El tall dura uns 30 minuts i el preu és 15 euros.'\n"
            "- Si el missatge no especifica cap servei o no és clar, respon amb una llista de tots els serveis amb durada i preu.\n"
            "- No inventis informació ni facis correccions, només el que hi ha a les dades.\n"
            "- Només has de respondre amb text clar i directe, res més.\n"
            "- Si et parla en català respons en català, si et parla en castellà en castellà"
        )

        completion = self.client.chat.completions.create(
            model = self.model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": message}
            ]
        )
        resposta = completion.choices[0].message.content.strip()
        return resposta


    def get_description_from_empleat(self, message, empleats):
        # Preparamos la lista de empleats para mostrar en la instrucción
        descriptions = "\n".join([f"- {e.nom}: {e.descripcio}" for e in empleats])
        prompt = (
            "Ets un assistent que rep un missatge on l'usuari pregunta per un empleat de perruqueria (ex: marc, joana, etc.) i/o "
            "vol saber la descripció de l'empleat.\n"
            f"La llista de empleats disponibles és:\n{descriptions}\n\n"
            "Instruccions:\n"
            "- Si el missatge conté clarament el nom d'un empleat, respon només amb una frase clara i concreta amb la descripció traduida a l'idioma que parli l'usuari"
            "Si no es un concret respon amb la descripció dels empleats.\n"
            "- Si el missatge no especifica cap empleat o no és clar, retorna ERROR"
            "HAS DE CONTESTAR EN EL IDIOMA EN EL QUE PARLA L'USUARI"
        )

        completion = self.client.chat.completions.create(
            model = self.model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": message}
            ]
        )
        resposta = completion.choices[0].message.content.strip()
        return resposta
        


