from enum import Enum
from models.basecontent import BaseContent,UpdateBaseContent
from typing import Union

class Car(BaseContent):
    plate: str
    make: str
    model: str
    year: int
    class Config:  
        arbitrary_types_allowed=True

class UpdateCar(UpdateBaseContent):
    plate: Union[str, None] = None
    make: Union[str, None] = None
    model: Union[str, None] = None
    year: Union[int, None] = None
    class Config:  
        arbitrary_types_allowed=True
