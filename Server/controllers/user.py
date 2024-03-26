from models.user import User, UpdateUser
from config.db import connection
from passlib.context import CryptContext
from fastapi import HTTPException
from models.user import Roles, Zones
from scripts.time import (
    bolivia_datetime_seconds,
    seconds_to_date                     
)
from bson import ObjectId

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

async def verify_username(username: str) -> dict:
    userFound = await connection.users.find_one({"username":username})
    if userFound != None:
        return  {"response": False, "detail": "User already exists"}
    if len(username) < 4:
        return  {"response": False, "detail": "Username is too short"}
    return {"response": True, "detail": "Ok"}

def verify_password(password: str) -> dict:
    if len(password) < 6:
        return {"response": False, "detail": "Password is too short"}
    return {"response": True, "detail": "Ok"}

def verify_names(name: str) -> dict:
    for character in name:
        if character.isdigit():
            return {"response": False, "detail": "Name can't contain numbers"}
    if len(name) < 3:
        return {"response": False, "detail": "Name is too short"}
    return {"response": True, "detail": "Ok"}

def verify_idzone(idzone: str) -> dict:
    values = [member.value for member in Zones]
    if not idzone in values:
        return  {"response": False, "detail": f'({idzone}) is not a valid zone'}
    return {"response": True, "detail": "Ok"}

async def verify_idnumber(idnumber: int,idzone: str) -> dict:
    userFound = await connection.users.find_one({"$and": [{"id_number":idnumber},{"id_zone":idzone}]})
    if userFound != None:
        return  {"response": False, "detail": "ID Number already exists"}
    return {"response": True, "detail": "Ok"}

async def verify_email(email) -> dict:
    if email != None:
        userFound = await connection.users.find_one({"email":email})
        if userFound != None:
            return  {"response": False, "detail": "Email already exists"}
    else:
        return {"response": True, "detail": "Ok"}

def verify_rol(rol: str) -> dict:
    values = [member.value for member in Roles]
    if not rol in values:
        return  {"response": False, "detail": f'({rol}) is not a valid rol'}
    return {"response": True, "detail": "Ok"}

def verify_getter_rol(getter: User):
    if ( (getter.rol != Roles.ADMIN.value) and (getter.rol != Roles.SUPERADMIN.value) and (getter.rol != Roles.TEACHER.value)):
        return  {"response": False, "detail": f'User {getter.first_name} does not have enough privileges'}
    return {"response": True, "detail": "Ok"}

async def verify_classroom(classroomId: str) -> dict:
    classroomFound = await connection.classrooms.find_one({"_id":ObjectId(classroomId)})
    if classroomFound == None:
        return  {"response": False, "detail": "Classroom does not exist"}
    return {"response": True, "detail": "Ok"}

def verify_birthday(birthday: int):
    if birthday > bolivia_datetime_seconds():
        return  {"response": False, "detail": f'{str(seconds_to_date(birthday))} is not a valid date'}
    return {"response": True, "detail": "Ok"}

async def validate_user(user: User):
    dict_user = dict(user)
    vrf = await verify_username(dict_user["username"])
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    vrf = verify_password(dict_user["password"])
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    vrf = verify_names(dict_user["first_name"])
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    vrf = verify_names(dict_user["father_last_name"])
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    vrf = verify_names(dict_user["mother_last_name"])
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    vrf = verify_idzone(dict_user["id_zone"])
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    vrf = await verify_idnumber(dict_user["id_number"],dict_user["id_zone"])
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    vrf = await verify_email(dict_user["email"])
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    vrf = verify_rol(dict_user["rol"])
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    vrf = verify_birthday(dict_user["birthday_date_inseconds"])
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )

async def validate_update_user(id: str,update_user:UpdateUser):
    actual_user = await connection.users.find_one({"_id": ObjectId(id)})

    dict_user = dict(update_user)
    vrf = {}
    new_user = {}
    for key, value in dict_user.items():
        if (value != None):
            match key:
                case "username":
                    vrf = await verify_username(value)
                case "password":
                    vrf = verify_password(value)
                case "first_name":
                    vrf = verify_names(value)
                case "father_last_name":
                    vrf = verify_names(value)
                case "mother_last_name":
                    vrf = verify_names(value)
                case "id_zone":
                    if(dict_user["id_number"] != None):
                        vrf = await verify_idnumber(dict_user["id_number"],value)
                    else:
                        vrf = verify_idzone(value)
                        if(vrf["response"]):
                            vrf = await verify_idnumber(actual_user["id_number"],value)
                case "id_number":
                    if(dict_user["id_zone"] != None):
                        vrf = await verify_idnumber(value,dict_user["id_zone"])
                    else:
                        vrf = await verify_idnumber(value,actual_user["id_zone"])  
                case "email":
                    vrf = await verify_email(value)
                case "rol":
                    vrf = await verify_rol(value)
                case "birthday_date_inseconds":
                    vrf = await verify_birthday(value)
                    
            if (not vrf["response"]):
                raise HTTPException(
                    status_code = 403, 
                    detail = vrf["detail"]
                )
            new_user[key] = value
    
    return new_user

async def get_all_users_controller(userLogged: User):
    vrf = verify_getter_rol(userLogged)    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403,
            detail = vrf["detail"]
        )
    users_async = connection.users.find().sort("father_last_name")
    users = []
    async for document in users_async:
        users.append(document)
    return users