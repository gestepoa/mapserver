from pydantic import BaseModel

class location(BaseModel):
    lon: float
    lat: float

class CircleMap(BaseModel):
    point1: location
    point2: location


class SeparateMap(BaseModel):
    name: list[str]


# fillin map model
class countryList(BaseModel):
    country: list[str]
    color: str
    note: str | None = None

class FillinMap(BaseModel):
    countryList: list[countryList]
    area: str | None = None
    range: list[int] | None = None
    boderColor: str | None = None
    worldColor: str | None = None
    boderWidth: float | None = None
    legendTitle: str | None = None

# map_points curd model
class PointCreate(BaseModel):
    spot_name: str
    latitude: float
    longitude: float
    height: float | None = None

class PointQuery(BaseModel):
    spot_name: list[str]

class PointUpdate(BaseModel):
    id: int
    spot_name: str | None = None
    spot_short_name: str | None = None
    spot_name_EN: str | None = None
    spot_short_name_EN: str | None = None
    country_name: str | None = None
    country_capital: str | None = None
    continental: str | None = None
    district: str | None = None
    note: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    height: float | None = None

class PointDelete(BaseModel):
    id: int