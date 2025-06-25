from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import models
from backend.database.database import engine
from backend.api.chatbot import ChatbotRouter
from backend.api.reserva import ReservaRouter
from backend.api.empleat import EmpleatRouter

# Crear les taules de la base de dades
models.Base.metadata.create_all(bind=engine)

# Inicialitzar FastAPI
app = FastAPI()

# Afegir middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_client_name = "groq"

# Incloure routers
app.include_router(ChatbotRouter(api_client_name).router)
app.include_router(ReservaRouter(api_client_name).router)
app.include_router(EmpleatRouter(api_client_name).router)