import json
from sqlalchemy.orm import Session
from . import models

def importar_dades_pelu(json_path: str, db: Session):
    print("obrint fitxer JSON...")
    with open(json_path, "r", encoding="utf-8") as f:
        contingut = f.read()
        print("Contingut llegit:", contingut[:100])  # Mostra només els primers 100 caràcters
        dades = json.loads(contingut)

    serveis_creats = {}

    # 1. Crear serveis generals si no existeixen
    for nom_servei in dades["serveis_generals"]:
        duracio = dades["temps_serveis"].get(nom_servei, 0)
        preu = dades["preus_serveis"].get(nom_servei, 0.0)

        servei = db.query(models.Servei).filter_by(nom=nom_servei).first()
        if not servei:
            servei = models.Servei(nom=nom_servei, duracio=duracio, preu=preu)
            db.add(servei)
            db.commit()
            db.refresh(servei)

        serveis_creats[nom_servei] = servei

    # 2. Crear empleats i associar serveis
    for e in dades["empleats"]:
        punts_forts_str = ", ".join(e["punts_forts"])

        empleat = models.Empleat(
            nom=e["nom"],
            descripcio=e["descripcio"],
            punts_forts=punts_forts_str
        )

        # Assignar serveis a l'empleat
        for servei_nom in e["serveis"]:
            servei = serveis_creats.get(servei_nom)
            if servei:
                empleat.serveis.append(servei)

        db.add(empleat)

    # 3. Crear horaris
    for dia, hores in dades["horari"].items():
        horari = db.query(models.Horari).filter_by(dia=dia).first()
        if not horari:
            horari = models.Horari(dia=dia, hores=hores)
            db.add(horari)

    db.commit()
