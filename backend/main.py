from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from backend.database import crud
from backend.database.read_json_pelu import importar_dades_pelu
from backend.google_calendar import create_event
from backend import chatbot
from backend.database import models
from backend.database.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELS ---

class Reserva(BaseModel):
    client_name: str = Field(..., example="Pol")
    service: str = Field(..., example="Tallat de cabells")
    iso_datetime: datetime = Field(..., example="2025-06-18T16:00:00")
    nom_empleat: str = Field(..., example="Marc")

class Message(BaseModel):
    message: str = Field(..., example="Em dic Carla")

# --- RUTES ---

@app.post("/bot_introduction")
def get_introduction():
    try:
        response = chatbot.get_bot_introduction()
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")

@app.post("/reserva")
def crear_reserva(reserva: Reserva):
    db = SessionLocal()
    try:
        duration_minutes = crud.get_minutes_for_service(db, reserva.service)
        if duration_minutes is None:
            raise HTTPException(status_code=400, detail=f"El servei {reserva.service} no existeix.")

        id_empleat = crud.get_empleat_id_by_name(db, reserva.nom_empleat)
        if id_empleat is None:
            raise HTTPException(status_code=400, detail=f"El empleat {reserva.nom_empleat} no existeix.")
        
        resultat = create_event(
            client_name=reserva.client_name,
            service=reserva.service,
            iso_datetime=reserva.iso_datetime,
            duration_minutes=duration_minutes,
        )
        crud.create_reserva(db, reserva.client_name, reserva.service, reserva.iso_datetime, duration_minutes, id_empleat)

        return {"message": "Reserva creada correctament", "event_id": resultat.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la reserva: {str(e)}")
    finally:
        db.close()

@app.post("/date_from_message")
def post_date(message: Message):
    try:
        response = chatbot.extract_date_from_message(message.message)
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")
    
@app.post("/name_from_message")
def post_name(message: Message):
    try:
        response = chatbot.extract_name_from_message(message.message)
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")
    
@app.post("/get_services")
def get_services():
    try:
        db = SessionLocal()
        services = crud.get_services(db)
        return {"message": services}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")
    
@app.post("/service_from_message")
def service_from_message(message: Message):
    try:
        db = SessionLocal()
        services = crud.get_services(db)
        response = chatbot.extract_service_from_message(message.message, services)
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")
    
@app.post("/get_empleat_from_message")
def empleat_from_message(message: Message):
    try:
        db = SessionLocal()
        empleats = crud.get_empleats_list(db)
        response = chatbot.extract_empleat_from_message(message.message, empleats)
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")

@app.post("/get_empleats_by_service")
def get_empleats(message: Message):
    try:
        db = SessionLocal()
        empleats = crud.get_empleats_by_service(db, message.message)
        return {"message": empleats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")


