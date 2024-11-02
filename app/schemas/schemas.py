from pydantic import BaseModel

class location(BaseModel):
    lon: float
    lat: float

class CircleMap(BaseModel):
    point1: location
    point2: location

class countryList(BaseModel):
    country: list[str]
    color: str
    note: str | None = None

class FillinMap(BaseModel):
    countryList: list[countryList]