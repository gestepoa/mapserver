from fastapi import APIRouter, Response, HTTPException, Depends
from app.schemas.schemas import CircleMap, FillinMap, PointCreate, PointQuery, PointUpdate, PointDelete
from app.utils.map_utils import generate_poi_image, generate_nightshade_image, generate_circle_image, fillin_color_image, fillin_color_image_pro
#db
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.database.model import MapPoint

router = APIRouter()

# curd api test
# add
@router.post("/map_points/add", response_model=PointCreate)
def create_point(point: PointCreate, db: Session = Depends(get_db)):
    db_point = MapPoint(**point.model_dump())
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point

# query
@router.post("/map_points/query")
async def query_map_points(point_query: PointQuery, db: Session = Depends(get_db)):
    if point_query.spot_name:
        points = db.query(MapPoint).filter(MapPoint.spot_name.in_(point_query.spot_name)).all()
        return {"success": True, "data": points}
    return {"success": False, "message": "No spot name provided."}

# update
@router.post("/map_points/update")
def update_map_point(point_update: PointUpdate, db: Session = Depends(get_db)):
    updated_point = db.query(MapPoint).filter(MapPoint.id == point_update.id).first()
    if updated_point:
        for key, value in point_update.dict(exclude_unset=True).items():
            setattr(updated_point, key, value)
        db.commit()
        db.refresh(updated_point)
    if updated_point:
        return {"success": "true", "data": updated_point}
    raise HTTPException(status_code=404, detail="Point not found")

@router.post("/map_points/delete")
def delete_map_point(point_delete: PointDelete, db: Session = Depends(get_db)):
    point = db.query(MapPoint).filter(MapPoint.id == point_delete.id).first()
    if point:
        db.delete(point)
        db.commit()
        return {"success": "true", "message": "Point deleted successfully"}
    raise HTTPException(status_code=404, detail="Point not found")
 

# map api
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
async def generate_map(request: FillinMap):
    try:
        output_path = fillin_color_image(request)
        return {
            "message": "success", 
            "status": 200,
            "local": output_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fillin_color_map/pro")
async def generate_map(request: FillinMap, db: Session = Depends(get_db)):
    try:
        output_path = fillin_color_image_pro(request, db)
        return {
            "message": "success", 
            "status": 200,
            "local": output_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
