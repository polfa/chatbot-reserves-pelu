from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import models
from backend.database.database import engine
from backend.api import chatbot, reserva, empleat

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot.router)
app.include_router(reserva.router)
app.include_router(empleat.router)
