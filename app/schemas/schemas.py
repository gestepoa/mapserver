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

# curd model
class PointCreate(BaseModel):
    spot_name: str
    country_name: str | None = None
    note: str | None = None
    latitude: float
    longitude: float
    height: float | None = None

class PointQuery(BaseModel):
    spot_name: list[str]

class PointUpdate(BaseModel):
    id: int
    spot_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None

class PointDelete(BaseModel):
    id: int