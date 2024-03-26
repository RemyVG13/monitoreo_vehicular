from enum import Enum
from models.basecontent import BaseContent,UpdateBaseContent
from typing import Union

class CarData(BaseContent):
    id_car: str
    date_in_seconds: int
    fuel: str
    longitude: float
    latitude: float
    speed: float
    class Config:  
        arbitrary_types_allowed=True

class UpdateCarData(UpdateBaseContent):
    id_car: Union[str, None] = None
    date: Union[int, None] = None
    fuel: Union[str, None] = None
    longitude: Union[float, None] = None
    latitude: Union[float, None] = None
    speed: Union[float, None] = None

    class Config:  
        arbitrary_types_allowed=True
