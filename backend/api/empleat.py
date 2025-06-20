from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.database.database import SessionLocal
from backend.database import crud
from backend.IA import chatbot
from backend.utils import utils

router = APIRouter()

class Message(BaseModel):
    message: str = Field(..., example="Amb la Carla")

@router.post("/get_empleat_from_message")
def empleat_from_message(message: Message):
    try:
        db = SessionLocal()
        empleats = crud.get_empleats_list(db)
        response = utils.extract_empleat_from_message(message.message, empleats)
        db.close()
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")

@router.post("/get_empleats_by_service")
def get_empleats(message: Message):
    try:
        db = SessionLocal()
        empleats = crud.get_empleats_by_service(db, message.message)
        db.close()
        return {"message": empleats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")
    

@router.post("/get_services")
def get_services():
    try:
        db = SessionLocal()
        services = crud.get_services(db)
        db.close()
        return {"message": services}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
