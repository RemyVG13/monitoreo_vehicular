from enum import Enum
from models.basecontent import BaseContent,UpdateBaseContent
from typing import Union
from pydantic import BaseModel

class Alarm(BaseContent):
    date: str
    hour: str
    reason: str
    teacher_name: str
    car_name: str
    thingspeak_id: int
    class Config:  
        arbitrary_types_allowed=True

class UpdateAlarm(UpdateBaseContent):
    date: Union[str, None] = None
    hour: Union[str, None] = None
    reason: Union[str, None] = None
    teacher_name: Union[str, None] = None
    car_name: Union[str, None] = None
    class Config:  
        arbitrary_types_allowed=True
        
class EmailRequest(BaseModel):
    sender_email: str
    sender_password: str
    receiver_email: str
    subject: str
    body: str
    attachment_path: str = None