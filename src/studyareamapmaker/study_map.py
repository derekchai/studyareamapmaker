from fastapi import FastAPI
from pydantic import BaseModel

class StudyMap(BaseModel):
    shapefile_path: str

    inset_width: float = 0.3
    inset_height: float = 0.3