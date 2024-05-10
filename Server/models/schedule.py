from enum import Enum
from models.basecontent import BaseContent,UpdateBaseContent
from typing import Union

class Days(Enum):
    SUNDAY = "Domingo"
    MONDAY = "Lunes"
    TUESDAY = "Martes"
    WEDNESDAY = "Miercoles"
    THURSDAY = "Jueves"
    FRIDAY = "Viernes"
    SATURDAY = "Sabado"

class Schedule(BaseContent):
    teacher_id: str
    car_id: str
    day: str #Day Class
    hour: int
    class Config:  
        arbitrary_types_allowed=True

class UpdateSchedule(UpdateBaseContent):
    teacher_id: Union[str, None] = None
    car_id: Union[str, None] = None
    day: Union[str, None] = None
    hour: Union[int, None] = None
    class Config:  
        arbitrary_types_allowed=True
