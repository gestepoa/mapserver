from fastapi import FastAPI
from app.api import map

app = FastAPI()

app.include_router(map.router, prefix="/maps")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Map API"}
