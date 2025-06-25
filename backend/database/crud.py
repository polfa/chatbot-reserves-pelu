from sqlalchemy.orm import Session
from . import models

def create_reserva(db: Session, client_n: str, serv: str, iso_datetime, duration_minutes: float, id_empleat: int):
    db_reserva = models.Reserva(
        client_name=client_n,
        service=serv,
        date=iso_datetime,
        duration=duration_minutes,
        empleat_id=id_empleat
    )
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)

def get_all_reserves(db: Session):
    return db.query(models.Reserva).all()

def get_empleat_id_by_name(db: Session, nom_empleat: str):
    empleat = db.query(models.Empleat).filter(models.Empleat.nom == nom_empleat).first()
    return empleat.id if empleat else None

def eliminar_reserva(db: Session, reserva_id: int):
    reserva = db.query(models.Reserva).filter_by(id=reserva_id).first()
    if not reserva:
        return False  # No existe la reserva
    db.delete(reserva)
    db.commit()
    return True  # Reserva eliminada

def get_services(db: Session):
    services = db.query(models.Servei).all()
    return ", ".join(service.nom for service in services)

def get_serveis_list(db: Session):
    serveis = db.query(models.Servei).all()
    return [servei.nom for servei in serveis]

def get_empleats_str(db: Session):
    empleats = db.query(models.Empleat).all()
    return ", ".join(empleat.nom for empleat in empleats)

def get_empleats_list(db: Session):
    empleats = db.query(models.Empleat).all()
    return [empleat for empleat in empleats]

def get_empleats_list_noms(db: Session):
    empleats = db.query(models.Empleat).all()
    return [empleat.nom for empleat in empleats]

def get_minutes_for_service(db: Session, service: str):
    servei = db.query(models.Servei).filter_by(nom=service).first()
    if servei:
        return servei.duracio
    return None

def get_empleats_by_service(db: Session, service: str):
    empleats = (
        db.query(models.Empleat)
        .join(models.Empleat.serveis)  # relació molts a molts amb la taula serveis
        .filter(models.Servei.nom == service)
        .all()
    )
    return [empleat.nom for empleat in empleats]

def get_all_services(db: Session):
    return db.query(models.Servei).all()

def get_descripcions_empleats(db: Session):
    return db.query(models.Empleat).all()
