from models.user import User, Roles
from config.db import connection
from passlib.context import CryptContext
from fastapi import HTTPException
from models.alarm import Alarm, UpdateAlarm
from scripts.time import (bolivia_datetime_seconds,
                          seconds_to_hhmm,
                          get_bolivia_date_time,
                          get_current_weekday_in_bolivia,
                          get_current_time_in_bolivia_seconds
                          )
from bson import ObjectId
from bson.regex import Regex

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

async def verify_alarm_id(id: str):
    res_id = await connection.alarms.find_one({"_id":ObjectId(id)})
    if res_id == None:
        return  {"response": False, "detail": "Alarm does not exist"}
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

def verify_creator_rol(creator: User):
    if ( (creator.rol != Roles.ADMIN.value) and (creator.rol != Roles.SUPERADMIN.value)):
        return  {"response": False, "detail": f'User {creator.first_name} does not have enough privileges'}
    return {"response": True, "detail": "Ok"}

def verify_getter_rol(getter: User):
    if ( (getter.rol != Roles.ADMIN.value) and (getter.rol != Roles.SUPERADMIN.value) and (getter.rol != Roles.TEACHER.value)):
        return  {"response": False, "detail": f'User {getter.first_name} does not have enough privileges'}
    return {"response": True, "detail": "Ok"}

'''
    date: str#
    hour: str#
    reason: str#
    teacher_name: str
    car_name: str#
    thingspeak_id: int#
'''
#CRUD functions
async def create_geoalarm_controller(alarm : Alarm, userLogged : User ):
    vrf = verify_creator_rol(userLogged)    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    dict_alarm = dict(alarm)
    actual_time = get_bolivia_date_time()
    actual_hour = get_current_time_in_bolivia_seconds()
    actual_weekday = get_current_weekday_in_bolivia()

    dict_alarm["date"] = actual_time["date"]
    dict_alarm["time"] = actual_time["time"]
    dict_alarm["reason"] = "Fuera de área"

    car = await connection.cars.find_one({"thingspeak_id":dict_alarm["thingspeak_id"]})
    dict_alarm["car_name"] = car["name"]
    schedules_async = connection.schedules.find({
            "$and": [
                { "car_id":car["id"] },
                { "day":actual_weekday}
            ]
        })
    
    schedules = []
    current_schedule={}
    async for document in schedules_async:
        schedules.append(document)

    if not schedules:
        dict_alarm["teacher_name"] = "Sin instructor"
    else:
        for schedule in schedules:
            if actual_hour <= (schedule["hour"] + 3600) and actual_hour >= (schedule["hour"]):
                current_schedule = schedule

    teacher_request = {}
    if not current_schedule:
        dict_alarm["teacher_name"] = "Sin instructor"
    else:
        teacher = await connection.users.find_one({"id":current_schedule["teacher_id"]})
        dict_alarm["teacher_name"] = teacher["first_name"] + " " + teacher["father_last_name"]

    
    dict_alarm["creation_date_inseconds"] = bolivia_datetime_seconds()
    dict_alarm["creator_id"] = str(userLogged.id)
    
    res = await connection.alarms.insert_one(dict_alarm)
    id = res.inserted_id
    await connection.alarms.update_one({"_id": ObjectId(id)}, {"$set": {"id":str(id)}})
    alarmdb = await connection.alarms.find_one({"_id": id})
    return alarmdb  

async def get_all_alarms_controller(userLogged: User,search:str):
    search_regex = Regex(search, "i")
    pipeline = [
        {
            "$match": {
                "$or": [
                    {"day": search_regex},
                    {"hour": search_regex},
                    {"teacher_name": search_regex},
                    {"car_name": search_regex},
                    {"reason": search_regex},
                ]
            }
        },
        {
            "$sort": {"day": 1}
        }
    ]

    alarms = []

    if search != "":
        async for document in connection.alarms.aggregate(pipeline):
            alarms.append(document)
    else:
        alarms_async = connection.alarms.find().sort("creation_date_inseconds")
        async for document in alarms_async:
            alarms.append(document)
    return alarms


