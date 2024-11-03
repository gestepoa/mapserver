from fastapi import FastAPI
from app.api import map
from app.database import model
from app.database.config import engine

model.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(map.router, prefix="/maps")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Map API"}
