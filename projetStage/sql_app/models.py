from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from projetStage.sql_app.database import Base


class User(Base):
    __tablename__ = "collaborateurs"

    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom=Column(String)
    compteur=Column(Integer)

    semaines = relationship("Semaine", back_populates="owner")


class Item(Base):
    __tablename__ = "semaines"

    id = Column(Integer, primary_key=True)
    numeroSemaine = Column(Integer)
    idCollaborateurs = Column(Integer, ForeignKey("collaborateurs.id"))

    owner = relationship("Collaborateur", back_populates="Semaine")
