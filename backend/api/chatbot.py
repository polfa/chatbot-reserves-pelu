from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.IA import chatbot
from backend.database import crud
from backend.database.database import SessionLocal

router = APIRouter()

class Message(BaseModel):
    message: str = Field(..., example="Em dic Carla")

@router.post("/bot_introduction")
def get_introduction():
    try:
        response = chatbot.get_bot_introduction()
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")

@router.post("/date_from_message")
def post_date(message: Message):
    try:
        response = chatbot.extract_date_from_message(message.message)
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")

@router.post("/name_from_message")
def post_name(message: Message):
    try:
        response = chatbot.extract_name_from_message(message.message)
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")

@router.post("/service_from_message")
def service_from_message(message: Message):
    try:
        db = SessionLocal()
        services = crud.get_services(db)
        response = chatbot.extract_service_from_message(message.message, services)
        db.close()
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")


@router.post("/get_services_info")
def get_services_info(message: Message):
    try:
        db = SessionLocal()
        services = crud.get_all_services(db)
        response = chatbot.get_services_info(message.message, services)
        db.close()
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")
