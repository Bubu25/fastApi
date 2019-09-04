from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.requests import Request
import graphene
from starlette.graphql import GraphQLApp
from enum import Enum
import uvicorn


# class Query(graphene.ObjectType):
#     hello = graphene.String(name=graphene.String(default_value="stranger"))
#
#     def resolve_hello(self, info, name):
#         return "helo "  +  name

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI(
    title="Pay for your coffee",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="2.5.0",
    openapi_url="/api/v1/openapi.json",
    #openapi_url=None)
    docs_url="/documentation"
)

# app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query)))
# app.mount("/static", StaticFiles(directory="static"), name="static")
#
# templates = Jinja2Templates(directory="templates")

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# @app.get("/items/{id}")
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}


uvicorn.run(app, port=8000, debug=True, access_log=False)