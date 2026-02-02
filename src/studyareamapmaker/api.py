import tempfile
import shutil
from fastapi import FastAPI, Response, UploadFile
from typing import List
from pathlib import Path
from .main import generate_study_area_map as get_changed_map

app = FastAPI()

@app.post("/get_map",
          responses={
              200: { "content": { "image/png": {} } }
          })
async def get_map(shapefiles: List[UploadFile]):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        main_shp_path = None

        for file in shapefiles:
            destination = temp_dir_path / file.filename
            with open(destination, "wb") as f:
                shutil.copyfileobj(file.file, f)

            if destination.suffix.lower() == ".shp":
                main_shp_path = destination

        image_bytes = get_changed_map(str(main_shp_path))
            
    return Response(content=image_bytes, media_type="image/png")
