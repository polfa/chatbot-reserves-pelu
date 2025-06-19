from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# --- Model reserva ---
class Reserva(Base):
    __tablename__ = "reserves"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, index=True)
    service = Column(String)
    date = Column(DateTime)
    duration = Column(Float)

    empleat_id = Column(Integer, ForeignKey("empleats.id"))
    empleat = relationship("Empleat", back_populates="reserves")

# --- Taula intermitja empleat-servei ---
empleat_servei = Table(
    "empleat_servei",
    Base.metadata,
    Column("empleat_id", Integer, ForeignKey("empleats.id")),
    Column("servei_id", Integer, ForeignKey("serveis.id")),
)

# --- Model empleat ---
class Empleat(Base):
    __tablename__ = "empleats"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    descripcio = Column(String)
    punts_forts = Column(String)

    serveis = relationship("Servei", secondary="empleat_servei", back_populates="empleats")
    reserves = relationship("Reserva", back_populates="empleat")

# --- Model servei ---
class Servei(Base):
    __tablename__ = "serveis"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, index=True)
    duracio = Column(Float)
    preu = Column(Float)

    empleats = relationship("Empleat", secondary=empleat_servei, back_populates="serveis")

# --- Model horari ---
class Horari(Base):
    __tablename__ = "horaris"

    id = Column(Integer, primary_key=True, index=True)
    dia = Column(String, unique=True)  # Ex: "dilluns"
    hores = Column(String)  # Ex: "10:00-19:00" o "TANCAT"
