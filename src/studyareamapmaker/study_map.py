import json
from pydantic import BaseModel, Field, model_validator

class StudyMap(BaseModel):
    inset_width: float = Field(default=0.3, ge=0, le=1)
    inset_height: float = Field(default=0.3, ge=0, le=1)

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value