from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.IA import chatbot
from backend.database import crud
from backend.database.database import SessionLocal

class Message(BaseModel):
    message: str = Field(..., example="Em dic Carla")

class ChatbotRouter:
    def __init__(self, api_client_name: str = "openai"):
        self.router = APIRouter()
        self.chatbotAPI = chatbot.ChatbotAPI(client_name=api_client_name)
        self._add_routes()

    def _add_routes(self):
        self.router.post("/bot_introduction")(self.get_introduction)
        self.router.post("/date_from_message")(self.post_date)
        self.router.post("/name_from_message")(self.post_name)
        self.router.post("/service_from_message")(self.service_from_message)
        self.router.post("/get_services_info")(self.get_services_info)

    def get_introduction(self):
        try:
            response = self.chatbotAPI.get_bot_introduction()
            return {"message": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")

    def post_date(self, message: Message):
        try:
            response = self.chatbotAPI.extract_date_from_message(message.message)
            return {"message": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")

    def post_name(self, message: Message):
        try:
            response = self.chatbotAPI.extract_name_from_message(message.message)
            return {"message": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")

    def service_from_message(self, message: Message):
        try:
            db = SessionLocal()
            services = crud.get_services(db)
            response = self.chatbotAPI.extract_service_from_message(message.message, services)
            db.close()
            return {"message": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")

    def get_services_info(self, message: Message):
        try:
            db = SessionLocal()
            services = crud.get_all_services(db)
            response = self.chatbotAPI.get_services_info(message.message, services)
            db.close()
            return {"message": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al resoldre la pregunta: {str(e)}")
