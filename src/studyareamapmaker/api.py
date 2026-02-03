import tempfile
import shutil
import base64
from fastapi import FastAPI, UploadFile, Request, Form, Depends
from typing import List, Annotated
from pathlib import Path
from studyareamapmaker import *
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from studyareamapmaker.study_map import StudyMapRegion, StudyMap
from studyareamapmaker.main import generate_study_area_map

app = FastAPI()

templates = Jinja2Templates(directory="templates")

def study_map_from_form(
    study_regions: List[StudyMapRegion] = Form(default=[]),
    title: str | None = Form(default=None),

    show_north_arrow: bool = Form(default=False),
    show_scale: bool = Form(default=False),
    show_axis_ticks: bool = Form(default=False),

    pad_top_factor: float = Form(default=0.1, ge=0),
    pad_bottom_factor: float = Form(default=0.1),
    pad_left_factor: float = Form(default=0.1),
    pad_right_factor: float = Form(default=0.1),

    inset_width: float = Form(default=0.3, ge=0, le=1),
    inset_height: float = Form(default=0.3, ge=0, le=1),
    inset_show_background: bool = Form(default=False),
    inset_line_width: float = Form(default=0.7, ge=0),
) -> StudyMap:
    return StudyMap(
        study_regions=study_regions,
        title=title,
        show_north_arrow=show_north_arrow,
        show_scale=show_scale,
        show_axis_ticks=show_axis_ticks,
        pad_top_factor=pad_top_factor,
        pad_bottom_factor=pad_bottom_factor,
        pad_left_factor=pad_left_factor,
        pad_right_factor=pad_right_factor,
        inset_width=inset_width,
        inset_height=inset_height,
        inset_show_background=inset_show_background,
        inset_line_width=inset_line_width
    )

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/get_map", response_class=HTMLResponse)
async def get_map(shapefiles: List[UploadFile],
                  study_map: Annotated[StudyMap, Depends] = Depends(study_map_from_form)):
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

    encoded_image = base64.b64encode(image_bytes).decode("utf-8")
    html = f'<img src="data:image/png;base64,{encoded_image}" alt="Study Map"/>'
            
    return HTMLResponse(content=html)
