from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from backend.google_calendar import create_event

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Afegir aquesta part abans de definir les rutes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O posa l'URL del teu frontend, ex: ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Reserva(BaseModel):
    client_name: str = Field(..., example="Pol")
    service: str = Field(..., example="Tallat de cabells")
    iso_datetime: datetime = Field(..., example="2025-06-18T16:00:00")
    duration_minutes: float = Field(..., example="30")

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
