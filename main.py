from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/eleve")
async def root():
    return{"message":"bubu"}

uvicorn.run(app, port=5000, debug=True, access_log=False)