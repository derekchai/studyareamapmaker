import json
from pydantic import BaseModel, Field, model_validator
from typing import List

class StudyMap(BaseModel):
    study_regions: List[StudyMapRegion] = Field(default=[])

    inset_width: float = Field(default=0.3, ge=0, le=1)
    inset_height: float = Field(default=0.3, ge=0, le=1)
    inset_show_background: bool = Field(default=False)
    inset_line_width: float = Field(default=0.7, ge=0)

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class StudyMapRegion(BaseModel):
    min_lat: float = Field(ge=-90, le=90)
    min_lon: float = Field(ge=-180, le=180)
    max_lat: float = Field(ge=-90, le=90)
    max_lon: float = Field(ge=-180, le=180)

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min_lat, self.min_lon, self.max_lat, self.max_lon \
                = min(self.min_lat, self.max_lat), \
                min(self.min_lon, self.max_lon), \
                max(self.min_lat, self.max_lat), \
                max(self.min_lon, self.max_lon)
