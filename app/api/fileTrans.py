from fastapi import APIRouter, HTTPException, File, UploadFile
# sys
import os
import kml2geojson
import json
import fiona

router = APIRouter()


@router.post("/kml2geojson")
async def upload_geojson(file: UploadFile = File(...)):
    if file.content_type not in [
        "application/geo+json",
        "application/json",
        "application/vnd.google-earth.kml+xml"
    ]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only GeoJSON or KML files are accepted.")

    print(file.filename)
    temp_file_path = f"./data/temp/temp_{file.filename}"
    output_geojson = f"./data/temp/test.json"

    try:
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())
  
        result = kml2geojson.main.convert(
            kml_path_or_buffer=temp_file_path,
            style_type=None,
            separate_folders=False
        )
        geojson_data = result[1] if len(result) > 1 else result
        with open(output_geojson, 'w', encoding='utf-8') as file:
            json.dump(geojson_data, file, indent=4, ensure_ascii=False)

        print(f"Conversion completed successfully. GeoJSON saved to: {output_geojson}")
        return {"success": True, "features_count": output_geojson}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")
    
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

