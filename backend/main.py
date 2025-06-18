from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from backend.google_calendar import create_event
from backend.chatbot import extract_date_from_message, extract_name_from_message, get_bot_introduction

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto por el origen de tu frontend si lo necesitas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS ---

class Reserva(BaseModel):
    client_name: str = Field(..., example="Pol")
    service: str = Field(..., example="Tallat de cabells")
    iso_datetime: datetime = Field(..., example="2025-06-18T16:00:00")
    duration_minutes: float = Field(..., example=30)

class Message(BaseModel):
    message: str = Field(..., example="Em dic Carla")

# --- RUTES ---

@app.post("/bot_introduction")
def get_introduction():
    try:
        response = get_bot_introduction()
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")

@app.post("/reserva")
def crear_reserva(reserva: Reserva):
    try:
        resultat = create_event(
            client_name=reserva.client_name,
            service=reserva.service,
            iso_datetime=reserva.iso_datetime,
            duration_minutes=reserva.duration_minutes,
        )
        return {"message": "Reserva creada correctament", "event_id": resultat.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la reserva: {str(e)}")

@app.post("/date_from_message")
def post_date(message: Message):
    try:
        response = extract_date_from_message(message.message)
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")
    
@app.post("/name_from_message")
def post_name(message: Message):
    try:
        response = extract_name_from_message(message.message)
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")
