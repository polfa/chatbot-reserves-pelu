

from database.crud import eliminar_reserva
from database.read_json_pelu import importar_dades_pelu
from database.database import SessionLocal, engine
from database import models


models.Base.metadata.create_all(bind=engine)

db = SessionLocal()
importar_dades_pelu("pelu_info.json", db)
db.close()