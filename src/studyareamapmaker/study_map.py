import json
import geopandas as gpd
from pydantic import BaseModel, Field, model_validator
from typing import List
from shapely.geometry import box

_WGS84 = "EPSG:4326"
_SPHERICAL_MERCATOR = "EPSG:3857"

class StudyMap(BaseModel):
    study_regions: List[StudyMapRegion] = Field(default=[])
    title: str | None = Field(default=None)

    show_north_arrow: bool = Field(default=True)
    show_scale: bool = Field(default=True)
    show_axis_ticks: bool = Field(default=True)

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

    def get_study_regions_data_frame_wgs84(self):
        data_frame = gpd.GeoDataFrame(
            { "name": [region.name or f"Region {i + 1}"
                       for i, region in enumerate(self.study_regions)] },
            geometry=[box(r.min_lon, r.min_lat, r.max_lon, r.max_lat) 
                    for r in self.study_regions],
            crs=_WGS84
        )

        data_frame_spherical_mercator = data_frame.to_crs(_SPHERICAL_MERCATOR)
        centroids = data_frame_spherical_mercator.centroid.to_crs(_WGS84)
        
        data_frame["centroid"] = centroids

        return data_frame

class StudyMapRegion(BaseModel):
    name: str | None = Field(default=None)

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
