from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.database.database import SessionLocal
from backend.database import crud
from backend.IA import chatbot
from backend.utils import utils

class Message(BaseModel):
    message: str = Field(..., example="Amb la Carla")

class EmpleatRouter:
    def __init__(self, api_client_name: str = "openai"):
        self.router = APIRouter()
        self.chatbotAPI = chatbot.ChatbotAPI(api_client_name)
        self._add_routes()

    def _add_routes(self):
        self.router.post("/get_empleat_from_message")(self.empleat_from_message)
        self.router.post("/get_empleats_by_service")(self.get_empleats)
        self.router.post("/get_services")(self.get_services)
        self.router.post("/get_descripcio_empleat")(self.get_descripcio_empleat)

    def empleat_from_message(self, message: Message):
        try:
            db = SessionLocal()
            empleats = crud.get_empleats_list_noms(db)
            response = self.chatbotAPI.extract_empleat_from_message(message.message, empleats)
            if response == "CONSULTA":
                empleats = crud.get_empleats_list(db)
                response = "[$C] " + self.chatbotAPI.get_description_from_empleat(message.message, empleats)
                return {"message": response}
            elif response == "NO":
                return {"message": "No s'ha trobat cap empleat que compleixi la consulta"}
            db.close()
            return {"message": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")

    def get_empleats(self, message: Message):
        try:
            db = SessionLocal()
            empleats = crud.get_empleats_by_service(db, message.message)
            db.close()
            return {"message": empleats}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")

    def get_services(self):
        try:
            db = SessionLocal()
            services = crud.get_services(db)
            db.close()
            return {"message": services}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    def get_descripcio_empleat(self, message: Message):
        try:
            db = SessionLocal()
            services = crud.get_descripcio_empleat(db, message.message)
            db.close()
            return {"message": services}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
