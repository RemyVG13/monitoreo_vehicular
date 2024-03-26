from models.user import Teacher, User, UpdateTeacher
from config.db import connection
from passlib.context import CryptContext
from fastapi import HTTPException
from models.user import Roles, Zones
from scripts.time import bolivia_datetime_seconds
from bson import ObjectId
from controllers.user import (
    validate_user,
    validate_update_user
)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

async def verify_teacher_id(id: str):
    res_id = await connection.users.find_one({"_id":ObjectId(id)})
    if res_id == None:
        return  {"response": False, "detail": "Teacher does not exist"}
    return {"response": True, "detail": "Ok"}

def verify_creator_rol(creator: User):
    if ( (creator.rol != Roles.ADMIN.value) and (creator.rol != Roles.SUPERADMIN.value)):
        return  {"response": False, "detail": f'User {creator.first_name} does not have enough privileges'}
    return {"response": True, "detail": "Ok"}

def verify_getter_rol(getter: User):
    if ( (getter.rol != Roles.ADMIN.value) and (getter.rol != Roles.SUPERADMIN.value) and (getter.rol != Roles.TEACHER.value)):
        return  {"response": False, "detail": f'User {getter.first_name} does not have enough privileges'}
    return {"response": True, "detail": "Ok"}

async def verify_getter_teacher(id: str, getter: Teacher):
    teacher_found = await connection.users.find_one({"_id": ObjectId(id)})
    getter_response = verify_getter_rol(getter)
    if ((teacher_found["username"] != getter.username) and not (getter_response["response"])):
        return  {"response": False, "detail": f'User {getter.first_name} does not have enough privileges'}
    return {"response": True, "detail": "Ok"}

async def create_teacher_controller(teacher : Teacher, userLogged : User ):
    dict_user = dict(teacher)
    await validate_user(teacher)

    vrf = verify_creator_rol(userLogged)    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
            
    dict_user["password"] = password_context.hash(dict_user["password"])
    dict_user["creation_date_inseconds"] = bolivia_datetime_seconds()
    dict_user["rol"] = Roles.TEACHER.value
    dict_user["creator_id"] = str(userLogged.id)
    res = await connection.users.insert_one(dict_user)
    id = res.inserted_id
    await connection.users.update_one({"_id": ObjectId(id)}, {"$set": {"id":str(id)}})
    userdb = await connection.users.find_one({"_id": id})
    return userdb

async def get_all_teachers_controller(userLogged: User):
    vrf = verify_getter_rol(userLogged)    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403,
            detail = vrf["detail"]
        )
    teachers_async = connection.users.find({"rol":Roles.TEACHER.value}).sort("father_last_name")
    teachers = []
    async for document in teachers_async:
        teachers.append(document)
    return teachers
    
async def get_teacher_controller(id: str,userLogged: User):
    vrf = await verify_teacher_id(id)    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    vrf = await verify_getter_teacher(id,userLogged) 
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    return await connection.users.find_one({"_id": ObjectId(id)})

async def update_teacher_controller(id: str,teacher: UpdateTeacher, userLogged: User):
    vrf = await verify_teacher_id(id)    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    dict_teacher = await validate_update_user(id,teacher)    
    
    vrf = verify_creator_rol(userLogged)
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )

    if("creation_date_inseconds" in dict_teacher):
        raise HTTPException(
            status_code = 403, 
            detail = "Creation date can not bet modified"
        )
    
    if("creator_id" in dict_teacher):
        raise HTTPException(
            status_code = 403, 
            detail = "Creator can not bet modified"
        )

    if("password" in dict_teacher):
        dict_teacher["password"] = password_context.hash(dict_teacher["password"])
    if("rol" in dict_teacher):
        dict_teacher["rol"] = Roles.TEACHER.value

    await connection.users.update_one(
            {"_id": ObjectId(id)}, {"$set": dict_teacher})
    
    return await connection.users.find_one({"_id": ObjectId(id)})

async def delete_teacher_controller(id: str,userLogged: User):
    vrf = await verify_teacher_id(id)    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    vrf = verify_creator_rol(userLogged)    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    await connection.users.delete_one({"_id": ObjectId(id)})

async def softdelete_teacher_controller(id: str,userLogged: User):
    vrf = await verify_teacher_id(id)    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    vrf = verify_creator_rol(userLogged)    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    await connection.users.update_one(
            {"_id": ObjectId(id)}, {"$set": {"deleted":True}})