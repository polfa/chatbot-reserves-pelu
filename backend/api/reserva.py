from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from backend.database.database import SessionLocal
from backend.database import crud
from backend.google.google_calendar import create_event

router = APIRouter()

class Reserva(BaseModel):
    client_name: str = Field(..., example="Pol")
    service: str = Field(..., example="Tallat de cabells")
    iso_datetime: datetime = Field(..., example="2025-06-18T16:00:00")
    nom_empleat: str = Field(..., example="Marc")

@router.post("/reserva")
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
        db.close()
        return {"message": "Reserva creada correctament", "event_id": resultat.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la reserva: {str(e)}")
    finally:
        db.close()
