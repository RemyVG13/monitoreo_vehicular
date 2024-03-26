from typing import Union
from enum import Enum
from models.basecontent import BaseContent, UpdateBaseContent
from pydantic import BaseModel
from bson import ObjectId
#paquete que interactua con la base de datos
class Roles(Enum):
    TEACHER = "teacher"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"

class Zones(Enum):
    LAPAZ = "LP"
    ORURO = "OR"
    POTOSI = "PT"
    PANDO = "PA"
    COCHABAMBA = "CB"
    CHUQUISACA = "CH"
    TARIJA = "TJ"
    SANTACRUZ = "SC"
    BENI = "BN"

class User(BaseContent):
    first_name: str
    father_last_name: Union[str, None] = None
    mother_last_name: Union[str, None] = None
    id_number: Union[int, None] = None
    id_zone: Union[str, None] = None #Zones Class
    username: str
    password : str
    birthday_date_inseconds: Union[int, None] = None
    rol: Union[str, None] = None

class UpdateUser(UpdateBaseContent):
    first_name: Union[str, None] = None
    father_last_name: Union[str, None] = None
    mother_last_name: Union[str, None] = None
    id_number: Union[int, None] = None
    id_zone: Union[str, None] = None #Zones Class
    username: Union[str, None] = None
    password : Union[str, None] = None
    birthday_date_inseconds: Union[int, None] = None
    rol: Union[str, None] = None

class Teacher(User):
    rol: str = Roles.TEACHER.value

class UpdateTeacher(UpdateUser):
    rol: Union[str, None] = Roles.TEACHER.value
    
class Admin(User):
    rol:str = Roles.ADMIN.value

class Superadmin(User):
    rol: str = Roles.SUPERADMIN.value


