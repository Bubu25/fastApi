from fastapi import FastAPI
from pydantic import BaseModel

import uvicorn


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None


app = FastAPI()


@app.post("/items/",response_model=Item)
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}", response_model=Item)
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

uvicorn.run(app, port=5000, debug=True, access_log=False)