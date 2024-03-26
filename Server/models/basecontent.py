from pydantic import BaseModel, Field
from typing import Union
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

class BaseContent(BaseModel):
    id: Union[str, None] = None
    disabled: bool = False
    creation_date_inseconds: Union[int, None] = None
    creator_id: Union[str, None] = None
    history_element: bool = False
    deleted: bool = False
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        #json_encoders = {ObjectId: str}

class UpdateBaseContent(BaseModel):
    disabled: Union[bool, None] = None
    creation_date_inseconds: Union[int, None] = None
    creator_id: Union[str, None] = None
    history_element: Union[bool, None] = None
    deleted: Union[bool, None] = None
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        #json_encoders = {ObjectId: str}
