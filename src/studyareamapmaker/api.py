import tempfile
import shutil
from fastapi import FastAPI, Response, UploadFile, Request
from typing import List
from pathlib import Path
from .main import generate_study_area_map 
from .study_map import StudyMap
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/get_map",
          responses={
              200: { "content": { "image/png": {} } }
          })
async def get_map(shapefiles: List[UploadFile],
                  study_map: StudyMap):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        main_shp_path = None

        for file in shapefiles:
            destination = temp_dir_path / file.filename
            with open(destination, "wb") as f:
                shutil.copyfileobj(file.file, f)

            if destination.suffix.lower() == ".shp":
                main_shp_path = destination

        image_bytes = generate_study_area_map(main_shp_path, study_map)
            
    return Response(content=image_bytes, media_type="image/png")
