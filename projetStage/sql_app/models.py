from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from projetStage.sql_app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom=Column(String)
    compteur=Column(Integer)

    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    Semaine_1 = Column(Integer)
    Semaine_2 = Column(Integer)
    Semaine_3 = Column(Integer)
    Semaine_4 = Column(Integer)
    Semaine_5 = Column(Integer)
    Semaine_6 = Column(Integer)
    Semaine_7 = Column(Integer)
    Semaine_8 = Column(Integer)
    Semaine_9 = Column(Integer)
    Semaine_10 = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
