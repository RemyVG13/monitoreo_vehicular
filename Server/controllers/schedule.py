from models.user import User, Roles
from config.db import connection
from passlib.context import CryptContext
from fastapi import HTTPException
from models.schedule import Schedule, UpdateSchedule, Days
from scripts.time import bolivia_datetime_seconds
from bson import ObjectId

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

async def verify_schedule_id(id: str):
    res_id = await connection.schedules.find_one({"_id":ObjectId(id)})
    if res_id == None:
        return  {"response": False, "detail": "Schedule does not exist"}
    return {"response": True, "detail": "Ok"}

async def verify_car_id(id: str) -> dict:
    car = await connection.cars.find_one({"_id":ObjectId(id)})
    if car == None:
        return  {"response": False, "detail": "Car does not exist"}
    return {"response": True, "detail": "Ok"}

async def verify_teacher_id(id: str) -> dict:
    teacher = await connection.users.find_one({"_id":ObjectId(id)})
    if teacher == None:
        return  {"response": False, "detail": "Teacher does not exist"}
    return {"response": True, "detail": "Ok"}


# async def verify_schedule_availability(id: str) -> dict:
#     schedule = await connection.schedules.find_one({"id":id})
#     if schedule != None:
#         return  {"response": False, "detail": "There are existing schedule for this item"}
#     return {"response": True, "detail": "Ok"}

def verify_creator_rol(creator: User):
    if ( (creator.rol != Roles.ADMIN.value) and (creator.rol != Roles.SUPERADMIN.value)):
        return  {"response": False, "detail": f'User {creator.first_name} does not have enough privileges'}
    return {"response": True, "detail": "Ok"}

def verify_getter_rol(getter: User):
    if ( (getter.rol != Roles.ADMIN.value) and (getter.rol != Roles.SUPERADMIN.value) and (getter.rol != Roles.TEACHER.value)):
        return  {"response": False, "detail": f'User {getter.first_name} does not have enough privileges'}
    return {"response": True, "detail": "Ok"}

def verify_day(day: str):
    values = [member.value for member in Days]
    if day not in values:
        return  {"response": False, "detail": f'{day} is not a valid day'}
    return {"response": True, "detail": "Ok"}



async def check_teacher_conflict(existing_schedule: dict, updated_schedule: dict) -> bool:
    # Verificar si el ID del profesor se está actualizando
    if updated_schedule.get("teacher_id") is not None and updated_schedule.get("teacher_id") != existing_schedule.get("teacher_id"):
        
        # Obtener los valores de day y hour actualizados, o mantener los valores originales si no se proporcionan
        updated_day = updated_schedule.get("day", existing_schedule.get("day"))
        updated_hour = updated_schedule.get("hour", existing_schedule.get("hour"))

        # Consultar horarios del profesor para el mismo día y hora
        conflicting_schedules = await connection.schedules.find({
            "day": updated_day,
            "hour": updated_hour,
            "teacher_id": updated_schedule["teacher_id"]
        }).to_list(length=None)
        if conflicting_schedules:
            return  {"response": False, "detail": f'There is a existing schedule for this teacher'}
    return {"response": True, "detail": f'Ok'}

async def check_car_conflict(existing_schedule: dict, updated_schedule: dict) -> bool:
    # Verificar si el ID del auto se está actualizando
    if updated_schedule.get("car_id") is not None and updated_schedule.get("car_id") != existing_schedule.get("car_id"):
    
        # Obtener los valores de day y hour actualizados, o mantener los valores originales si no se proporcionan
        updated_day = updated_schedule.get("day", existing_schedule.get("day"))
        updated_hour = updated_schedule.get("hour", existing_schedule.get("hour"))

        # Consultar horarios del auto para la misma hora y día
        conflicting_schedules = await connection.schedules.find({
            "day": updated_day,
            "hour": updated_hour,
            "car_id": updated_schedule["car_id"]
        }).to_list(length=None)
        if conflicting_schedules:
            return  {"response": False, "detail": f'There is a existing schedule for this car'}
    return {"response": True, "detail": f'Ok'}




#CRUD functions
async def create_schedule_controller(schedule : Schedule, userLogged : User ):
    dict_schedule = dict(schedule)

    vrf = verify_creator_rol(userLogged)    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    vrf = await verify_teacher_id(dict_schedule["teacher_id"])    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    vrf = await verify_car_id(dict_schedule["car_id"])    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )

    dict_schedule["creation_date_inseconds"] = bolivia_datetime_seconds()
    dict_schedule["creator_id"] = str(userLogged.id)
        
    res = await connection.schedules.insert_one(dict_schedule)
    id = res.inserted_id
    await connection.schedules.update_one({"_id": ObjectId(id)}, {"$set": {"id":str(id)}})
    scheduledb = await connection.schedules.find_one({"_id": id})
    return scheduledb

async def get_all_schedules_controller(userLogged: User):
    schedules_async = connection.schedules.find()
    schedules = []
    async for document in schedules_async:
        schedules.append(document)
    return schedules
    
async def get_schedule_controller(id: str,userLogged: User):
    vrf = await verify_schedule_id(id)    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    return await connection.schedules.find_one({"_id": ObjectId(id)})
    

async def update_schedule_controller(id: str,schedule: UpdateSchedule, userLogged: User):
    vrf = await verify_schedule_id(id)    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )

    original_schedule = await connection.schedules.find_one({"_id":ObjectId(id)})
    dict_original_schedule = dict(original_schedule)
    dict_schedule = dict(schedule)
    vrf = {}
    update_schedule = {}
    for key, value in dict_schedule.items():
        if (value != None):
            update_schedule[key] = value
    
    vrf = verify_creator_rol(userLogged)
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    if("creation_date_inseconds" in update_schedule):
        raise HTTPException(
            status_code = 403, 
            detail = "Creation date can not bet modified"
        )
    
    if("creator_id" in update_schedule):
        raise HTTPException(
            status_code = 403, 
            detail = "Creator can not bet modified"
        )

    if "car_id" in update_schedule:
        vrf = verify_car_id(update_schedule["car_id"])
        if (not vrf["response"]):
            raise HTTPException(
                status_code = 403, 
                detail = vrf["detail"]
            )
        
    if "teacher_id" in update_schedule:
        vrf = verify_teacher_id(update_schedule["teacher_id"])
        if (not vrf["response"]):
            raise HTTPException(
                status_code = 403, 
                detail = vrf["detail"]
            )
    
    vrf = await check_teacher_conflict(dict_original_schedule, update_schedule)
    if (not vrf["response"]):
            raise HTTPException(
                status_code = 403, 
                detail = vrf["detail"]
            )  

    vrf = await check_car_conflict(dict_original_schedule, update_schedule)
    if (not vrf["response"]):
            raise HTTPException(
                status_code = 403, 
                detail = vrf["detail"]
            )  

    
    await connection.schedules.update_one(
            {"_id": ObjectId(id)}, {"$set": update_schedule})
    
    return await connection.schedules.find_one({"_id": ObjectId(id)})

async def delete_schedule_controller(id: str,userLogged: User):
    vrf = await verify_schedule_id(id)
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
    
    await connection.schedules.delete_one({"_id": ObjectId(id)})

async def softdelete_schedule_controller(id: str,userLogged: User):
    vrf = await verify_schedule_id(id)    
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
    
    await connection.schedules.update_one(
            {"_id": ObjectId(id)}, {"$set": {"deleted":True}})