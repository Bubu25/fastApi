from typing import List
from pydantic import BaseModel

class ItemBase(BaseModel):
    Semaine_1: int
    Semaine_2: int
    Semaine_3: int
    Semaine_4: int
    Semaine_5: int
    Semaine_6: int
    Semaine_7: int
    Semaine_8: int
    Semaine_9: int
    Semaine_10:int


class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    #id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    nom: str
    prenom: str
    compteur: int


class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True