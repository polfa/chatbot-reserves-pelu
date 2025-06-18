# backend/chatbot.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_bot_response(user_input):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Ets un assistent virtual per una perruqueria. Respon amb simpatia i de forma clara."},
            {"role": "user", "content": user_input},
        ]
    )
    return completion.choices[0].message.content
