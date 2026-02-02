from pydantic import BaseModel, Field

class StudyMap(BaseModel):
    inset_width: float = Field(default=0.3, ge=0, le=1)
    inset_height: float = Field(default=0.3, ge=0, le=1)