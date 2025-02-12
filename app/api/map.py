from fastapi import APIRouter, Response, HTTPException, Depends, File, UploadFile
from app.schemas.schemas import CircleMap, FillinMap, PointCreate, PointQuery, PointUpdate, PointDelete, SeparateMap
from app.utils.map_utils import generate_poi_image, generate_nightshade_image, generate_circle_image, fillin_color_image, fillin_color_image_pro, draw_polyline, generate_separate_image
#db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.config import get_db
from app.database.model import MapPoint
# sys
import os
import kml2geojson
import json

router = APIRouter()

# map_points curd api
# add
@router.post("/map_points/add", response_model=PointCreate)
async def create_point(point: PointCreate, db: AsyncSession = Depends(get_db)):
    db_point = MapPoint(**point.model_dump())
    db.add(db_point)
    await db.commit()
    await db.refresh(db_point)
    return db_point

# query
@router.post("/map_points/query")
async def query_map_points(point_query: PointQuery, db: AsyncSession = Depends(get_db)):
    if point_query.spot_name:
        result = await db.execute(
            select(MapPoint).where(MapPoint.spot_name.in_(point_query.spot_name))
        )
        points = result.scalars().all()
        return {"success": True, "data": points}
    return {"success": False, "message": "No spot name provided."}

# update
@router.post("/map_points/update")
async def update_map_point(point_update: PointUpdate, db: AsyncSession = Depends(get_db)):
    query = select(MapPoint).where(MapPoint.id == point_update.id)
    result = await db.execute(query)
    updated_point = result.scalars().first()
    if updated_point:
        for key, value in point_update.model_dump(exclude_unset=True).items():
            setattr(updated_point, key, value)
        await db.commit()
        await db.refresh(updated_point)
    if updated_point:
        return {"success": "true", "data": updated_point}
    raise HTTPException(status_code=404, detail="Point not found")

@router.post("/map_points/delete")
async def delete_map_point(point_delete: PointDelete, db: AsyncSession = Depends(get_db)):
    query = select(MapPoint).where(MapPoint.id == point_delete.id)
    result = await db.execute(query)
    point = result.scalars().first()
    if point:
        await db.delete(point)
        await db.commit()
        return {"success": "true", "message": "Point deleted successfully"}
    raise HTTPException(status_code=404, detail="Point not found")
 

# map api
@router.post("/poi_map/")
async def generate_map():
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
    

@router.post("/separate_map/")
async def generate_map(request: SeparateMap, db: AsyncSession = Depends(get_db)):
    try:
        output_path = await generate_separate_image(request, db)
        return {
            "message": "success", 
            "status": 200,
            "local": output_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/fillin_color_map/")
async def generate_map(request: FillinMap, db: AsyncSession = Depends(get_db)):
    try:
        output_path = await fillin_color_image(request, db)
        return {
            "message": "success", 
            "status": 200,
            "local": output_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fillin_color_map/pro")
async def generate_map(request: FillinMap, db: AsyncSession = Depends(get_db)):
    try:
        output_path = await fillin_color_image_pro(request, db)
        return {
            "message": "success", 
            "status": 200,
            "local": output_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/polyline_map/")
async def upload_geojson(file: UploadFile = File(...)):
    if file.content_type != "application/geo+json" and file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="Invalid file type. Only GeoJSON files are accepted.")

    temp_file_path = f"./data/temp/temp_{file.filename}"

    try:
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())
  
        processed_data = await draw_polyline(temp_file_path)
        
        return {"success": True, "features_count": processed_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")
    
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

