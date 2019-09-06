#### Api avec FastAPi
### Objectifs: déterminer qui paye son café chaque semaine au sein d'une équipe
### Les données sont stockées dans une base données de type sqlite
### la sélection se fait au hasard pour respecter l'équité.
### chaque utilisateur indique sa présence ou nom pour les différentes semaines

from typing import List
import random
import uvicorn
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
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    print(db_user.nom, db_user.prenom, db_user.compteur)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/items/{user_id}", response_model=schemas.Item)
def read_item(user_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, user_id=user_id)
    print(item.__dict__)
    return item

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

#####début algo pour la sélection des payeurCoffee

    ###commandes testées:
    #[Semaines.append(i) for i in users[1].items[0].__dict__.keys() if "Semaine" in i]
    # print(list(users[1].items[0].__dict__.values())) !!attention ne renvoie pas valeurs correspondant pas à la data base
    #print(users[0].items[0].__dict__.keys())
    #[print(i) for i in users[0].items[0].__dict__ if "Semaine" in i]
    #print

    ###initialisations des différentes variables########################

    ###1ere variables initialisées
    Semaines=[]
    valeurs=[]
    dicoNbreSemaine={}
    nombreUsers=len(users)

    ### calcul nbre de semaines présent pour chaque utilisateur
    for u in range(0,nombreUsers):
        for i in users[u].items[0].__dict__.keys():
            if "Semaine" in i:
                valeurs.append(users[u].items[0].__dict__[i])
        nombreSemainesPresent=sum(valeurs)
        dicoNbreSemaine['user '+str(u+1)]=nombreSemainesPresent
        valeurs=[]

    #2ème variables initialisées
    [Semaines.append(i) for i in users[1].items[0].__dict__.keys() if "Semaine" in i]
    nombreSemaines = len(Semaines)
    listNomUsers=[]
    listePayeurs=[]

    ### initialisation des compteurs à zéro
    dicoCompteur={}
    for u in users:
        dicoCompteur[u.nom]=u.compteur # dico avec le nom comme clé et le compteur coffee comme valeur

    print(dicoCompteur)
    print("nombre de semaines présent:",dicoNbreSemaine)


    ## début selection########################################################

    i = 0 # indice associée au compteur coffee
    for s in range(1,nombreSemaines+1):
        for u in users:
            presence=getattr(u.items[0], "Semaine_" + str(s))
            if presence==1 and dicoCompteur[u.nom]<=i:
                listNomUsers.append(u.nom)
        ##si pas de Noms dans la liste i s'incrémente de +1 pour trouver user avec un compteur coffee supérieur
        if listNomUsers ==[]:
            j=0
            while listNomUsers ==[]:
                i+=1
                j+=1
                for u in users:
                    presence = getattr(u.items[0], "Semaine_" + str(s))
                    if presence== 1 and dicoCompteur[u.nom] <= i:
                        listNomUsers.append(u.nom)
            i-=j ### i reprendre sa valeur initial par l'intermédiaire de j
            j=0
        if listNomUsers!=[]:
            payeur=random.choice(listNomUsers)
            #print("payeur 1:",payeur)
            if s!=1:## entre en action à partir de la 2ème semaine
                if payeur==listePayeurs[len(listePayeurs)-1] and len(listNomUsers)!=1: ## evite qu'un utilisateur paye 2 fois de suite
                    while payeur==listePayeurs[len(listePayeurs)-1]:
                        payeur=random.choice(listNomUsers)
                        #print("payeur 2:",payeur)
        else:
            Semaine_N="Semaine_"+str(s)
            return f"{Semaine_N} pas de payeur, relancer la sélection"

        dicoCompteur[payeur]=dicoCompteur[payeur]+1
        listePayeurs.append(payeur)
        # print('liste payeur : ',listePayeurs)
        # print(dicoCompteur)


        ##si tous les users ont le même compteur, i s'incrémente de 1
        listCompteurCoffee = []
        for c in dicoCompteur:
            cpt = dicoCompteur.get(c)
            listCompteurCoffee.append(cpt)
        if i not in listCompteurCoffee:
            i +=1
        listNomUsers = []

#####fin algo selection payeurCoffee

    print("noms utilisateurs et nombre de fois payés:",dicoCompteur)

    #return f"les  payeurs par semaine classés dans l'orde des semaines croissantes sont {listePayeurs}"
    return f"les coffeePayeurs sont {dicoCompteur}"

uvicorn.run(app, port=8000, debug=True, access_log=False)