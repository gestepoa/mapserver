from fastapi import APIRouter, Response, HTTPException
from app.utils.map_utils import generate_poi_image, generate_nightshade_image, generate_circle_image

router = APIRouter()

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
async def generate_map():
    try:
        output_path = generate_circle_image()
        return {
            "message": "success", 
            "status": 200,
            "local": output_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
