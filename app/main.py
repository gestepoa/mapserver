from fastapi import FastAPI
from app.api import map
from app.database.config import close_all
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting...")
    yield
    print("Application shutting down...")
    await close_all()

app = FastAPI(lifespan=lifespan)

app.include_router(map.router, prefix="/maps")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Map API"}
