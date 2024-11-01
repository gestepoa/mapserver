from fastapi import APIRouter, Response, HTTPException
from pydantic import BaseModel
from app.utils.map_utils import generate_poi_image, generate_nightshade_image, generate_circle_image, fillin_color_image

router = APIRouter()

class location(BaseModel):
    lon: float
    lat: float

class CircleMap(BaseModel):
    point1: location
    point2: location

class FillinMap(BaseModel):
    point: list[location]

@router.post("/poi_map/")
def generate_map():
    img_buffer = generate_poi_image()
    return Response(content=img_buffer.getvalue(), media_type="image/jpeg")

@router.post("/nightshade_map/")
async def generate_map():
    try:
        output_path = generate_nightshade_image()
        return {
            "message": "success", 
            "status": 200,
            "local": output_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/circle_map/")
async def generate_map(request: CircleMap):
    try:
        output_path = generate_circle_image(request.point1.lon, request.point1.lat, request.point2.lon, request.point2.lat)
        return {
            "message": "success", 
            "status": 200,
            "local": output_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/fillin_color_map/")
async def generate_map():
    try:
        output_path = fillin_color_image()
        return {
            "message": "success", 
            "status": 200,
            "local": output_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
