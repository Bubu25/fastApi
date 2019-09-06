from sqlalchemy.orm import Session
from projetStage.sql_app import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_item(db: Session, user_id: int):
    return db.query(models.Item).filter(models.Item.id == user_id).first()


def get_user_by_nom(db: Session, nom:str):
    return db.query(models.User).filter(models.User.nom == nom).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_update(db:Session, user_id:int, user: schemas.UserUpdate):
    db.query(models.User).filter(models.User.id == user_id).first()
    up=models.User(nom=user.nom, prenom=user.prenom, compteur=user.compteur)
    db_user = up
    db._u(db_user)
    db.commit()
    db.refresh(db_user)
    return

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(nom=user.nom, prenom=user.prenom,compteur=user.compteur)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item