from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Annotated

class StudyMap(BaseModel):
    inset_width: Annotated[float, Query(ge=0, le=1)] = 0.3
    inset_height: Annotated[float, Query(ge=0, le=1)] = 0.3