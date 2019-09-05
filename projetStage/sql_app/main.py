#### Api avec FastAPi
### Objectifs: déterminer qui paye son café chaque semaine au sein d'une équipe
### Les données sont stockées dans une base données de type sqlite
### la sélection se fait au hasard pour respecter l'équité.
### chaque utilisateur indique sa présence ou nom pour les différentes semaines

from typing import List
import random
import uvicorn
import operator
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response

from projetStage.sql_app import crud, models, schemas
from projetStage.sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Dependency
def get_db(request: Request):
    return request.state.db


### post pour entrer le nom, prénom et  le compteur( nombre de fois où le café est payé par
## l'utilisateur: initialement valeur entré =0)
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_nom(db, nom=user.nom)
    if db_user:
        raise HTTPException(status_code=400, detail="Nom already registered")
    return crud.create_user(db=db, user=user)

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id:int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user_update(db=db, user_id=user_id, user=user)
    #print(db_user.nom, db_user.prenom, db_user.compteur)
    return db_user

### lecture par id de chaque utilisateur
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db), q:str=None):
    print(q)
    db_user = crud.get_user(db, user_id=user_id)
    print(db_user.nom, db_user.prenom, db_user.compteur)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

### lecture de la base de données
### retourne à la fois les infos de l'utilisateurs et les infos sur sa présence ou nom pour chaque semaine
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    print(len(users),users[0].nom, users[0].items[0].Semaine_1)
    return users

### l'utilisateur indique sa présence ou non pour les différentes semaines
### l'utilisateur doit indiquer 0 pour absence et 1 pour présence pour chaque semaine
@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

### affiche une liste contenant comment élément  l'id user et son calendrier de présence
### pour les différentes semaines.
@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


##### Selection par semaine de la personne qui paye le café,
#### Personne nommée: payeur
@app.get("/selection")
async def selection_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    print(len(users), users[0].nom, users[0].items[0].Semaine_1)

    nombreSemaines = 10
    listNomUsers_S1=[]
    listNomUsers_S2=[]
    listNomUsers_S3=[]
    listNomUsers_S4=[]
    listNomUsers_S5=[]
    listNomUsers_S6=[]
    listNomUsers_S7=[]
    listNomUsers_S8=[]
    listNomUsers_S9=[]
    listNomUsers_S10=[]
    listePayeur=[]
    cpt_User1=0
    cpt_User2=0
    cpt_User3=0
    cpt_User4=0
    cpt_User5=0
    dico={}
    cpt =0
    i=0
    dico={}

    for u in users:
        dico[u.nom]=0
    print(dico)

    for u in users:
        if cpt!=0 and ((cpt % nombreSemaines) == 0 or (nombreSemaines % cpt) == 0):
            i=+1
        if u.items[0].Semaine_1==1 and dico[u.nom]==i: #### conditions qui vérifie si user est présent ou pas et
            listNomUsers_S1.append(u.nom)
    #if listNomUsers_S1 ==[]:

    payeur_S1=random.choice(listNomUsers_S1)
    dico[payeur_S1]=dico[payeur_S1]+1
    dico_trie = sorted(dico.items(), reverse=True, key=operator.itemgetter(1))

    print(dico_trie, payeur_S1)
    listePayeur.append(payeur_S1)
    print(i)
    cpt=+1

    for u in users:
        #print(u.items[0].Semaine_2)
        if cpt!=0 and ((cpt%nombreSemaines)==0 or (nombreSemaines%cpt)==0):
            i=+1
        if u.items[0].Semaine_2==1 and dico[u.nom]==i:
            listNomUsers_S2.append(u.nom)

    payeur_S2=random.choice(listNomUsers_S2)
    dico[payeur_S2] = dico[payeur_S2] + 1
    print(dico,payeur_S2)
    listePayeur.append(payeur_S2)
    print(i)
    cpt=+1

    for u in users:
        #print(u.items[0].Semaine_3)
        if cpt!=0 and ((cpt % nombreSemaines) == 0 or (nombreSemaines % cpt) == 0):
            i=+1
        if u.items[0].Semaine_3==1 and dico[u.nom]==i:
            listNomUsers_S3.append(u.nom)
    payeur_S3=random.choice(listNomUsers_S3)
    dico[payeur_S3] = dico[payeur_S3] + 1
    print(dico,payeur_S3)
    listePayeur.append(payeur_S3)
    print(i)
    cpt=+1

    for u in users:
        #print(u.items[0].Semaine_4)
        if cpt!=0 and ((cpt % nombreSemaines) == 0 or (nombreSemaines % cpt) == 0):
            i=+1
        if u.items[0].Semaine_4 == 1 and dico[u.nom]==i:
            listNomUsers_S4.append(u.nom)
    payeur_S4 = random.choice(listNomUsers_S4)
    dico[payeur_S4] = dico[payeur_S4] + 1
    print(dico, payeur_S4)
    listePayeur.append(payeur_S4)
    cpt = +1

    for u in users:
        #print(u.items[0].Semaine_5)
        if cpt!=0 and ((cpt % nombreSemaines) == 0 or (nombreSemaines % cpt) == 0):
            i=+1
        if u.items[0].Semaine_5 == 1 and dico[u.nom]==i:
            listNomUsers_S5.append(u.nom)
    payeur_S5 = random.choice(listNomUsers_S5)
    dico[payeur_S5] = dico[payeur_S5] + 1
    print(dico,payeur_S5)
    listePayeur.append(payeur_S5)
    cpt = +1

    for u in users:
        #print(u.items[0].Semaine_6)
        if cpt!=0 and ((cpt % nombreSemaines) == 0 or (nombreSemaines % cpt) == 0):
            i=+1
        if u.items[0].Semaine_6 == 1 and dico[u.nom]==i:
            listNomUsers_S6.append(u.nom)
    payeur_S6 = random.choice(listNomUsers_S6)
    dico[payeur_S6] = dico[payeur_S6] + 1
    print(dico,payeur_S6)
    listePayeur.append(payeur_S6)
    cpt = +1

    for u in users:
        #print(u.items[0].Semaine_7)
        if cpt!=0 and ((cpt % nombreSemaines) == 0 or (nombreSemaines % cpt) == 0):
            i=+1
        if u.items[0].Semaine_7 == 1 and dico[u.nom]==i:
            listNomUsers_S7.append(u.nom)
    payeur_S7 = random.choice(listNomUsers_S7)
    dico[payeur_S7] = dico[payeur_S7] + 1
    print(dico, payeur_S7)
    listePayeur.append(payeur_S7)
    cpt = +1

    for u in users:
        #print(u.items[0].Semaine_8)
        if cpt!=0 and ((cpt % nombreSemaines) == 0 or (nombreSemaines % cpt) == 0):
            i=+1
        if u.items[0].Semaine_8 == 1 and dico[u.nom]==i:
            listNomUsers_S8.append(u.nom)
    payeur_S8 = random.choice(listNomUsers_S8)
    dico[payeur_S8] = dico[payeur_S8] + 1
    print(dico, payeur_S8)
    listePayeur.append(payeur_S8)
    cpt = +1

    for u in users:
        #print(u.items[0].Semaine_9)
        if cpt!=0 and ((cpt % nombreSemaines) == 0 or (nombreSemaines % cpt) == 0):
            i=+1
        if u.items[0].Semaine_9 == 1 and dico[u.nom]==i:
            listNomUsers_S9.append(u.nom)
    payeur_S9 = random.choice(listNomUsers_S9)
    dico[payeur_S9] = dico[payeur_S9] + 1
    print(dico, payeur_S9)
    listePayeur.append(payeur_S9)
    cpt = +1

    for u in users:
        #print(u.items[0].Semaine_10)
        if cpt!=0 and ((cpt % nombreSemaines) == 0 or (nombreSemaines % cpt) == 0):
            i=+1
        if u.items[0].Semaine_10 == 1 and dico[u.nom]==i:
            listNomUsers_S10.append(u.nom)
    payeur_S10 = random.choice(listNomUsers_S10)
    dico[payeur_S10] = dico[payeur_S10] + 1
    print(dico, payeur_S10)
    listePayeur.append(payeur_S10)
    cpt = +1

    print(dico)


    @app.put("/users/", response_model=List[schemas.User])
    def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        users = crud.get_users(db, skip=skip, limit=limit)
        print(len(users), users[0].nom, users[0].items[0].Semaine_1)
        return users
    #print(users[0].nom)


    return f"les  payeurs sont {listePayeur}"



uvicorn.run(app, port=8000, debug=True, access_log=False)