from models.user import User, Roles
import datetime
from config.db import connection
from passlib.context import CryptContext
from fastapi import HTTPException
from models.car import Car, UpdateCar
from scripts.time import (
    bolivia_datetime_seconds,
    iso_to_local_time,
    get_current_time_in_bolivia_seconds,
    get_current_weekday_in_bolivia,
    is_within_last_minute,
    convert_to_bolivia_time
    )
from scripts.geo import is_point_in_polygon
from bson import ObjectId
from bson.regex import Regex
import requests

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

async def verify_car_id(id: str):
    res_id = await connection.cars.find_one({"_id":ObjectId(id)})
    if res_id == None:
        return  {"response": False, "detail": "Car does not exist"}
    return {"response": True, "detail": "Ok"}

async def verify_plate(plate: str):
    res = await connection.cars.find_one({"plate":plate})
    if res != None:
        return  {"response": False, "detail": "Car plate already exist"}
    return {"response": True, "detail": "Ok"}

def verify_creator_rol(creator: User):
    if ( (creator.rol != Roles.ADMIN.value) and (creator.rol != Roles.SUPERADMIN.value)):
        return  {"response": False, "detail": f'User {creator.first_name} does not have enough privileges'}
    return {"response": True, "detail": "Ok"}

def verify_getter_rol(getter: User):
    if ( (getter.rol != Roles.ADMIN.value) and (getter.rol != Roles.SUPERADMIN.value) and (getter.rol != Roles.TEACHER.value)):
        return  {"response": False, "detail": f'User {getter.first_name} does not have enough privileges'}
    return {"response": True, "detail": "Ok"}

async def check_car_conflict(existing_car: dict, updated_car: dict) -> bool:
    # Verificar si el ID del auto se está actualizando
    if updated_car.get("plate") is not None and updated_car.get("plate") != existing_car.get("plate"):
        
        # Obtener los valores de day y hour actualizados, o mantener los valores originales si no se proporcionan
        updated_plate = updated_car.get("plate", existing_car.get("plate"))

        # Consultar horarios del auto para la misma hora y día
        conflicting_cars = await connection.cars.find({
            "day": updated_plate
        }).to_list(length=None)
        if conflicting_cars:
            return  {"response": False, "detail": f'There is a existing plate for this car'}
    return {"response": True, "detail": f'Ok'}




#CRUD functions
async def create_car_controller(car : Car, userLogged : User ):
    dict_car = dict(car)

    vrf = verify_creator_rol(userLogged)    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    vrf = await verify_plate(dict_car["plate"])    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )

    dict_car["creation_date_inseconds"] = bolivia_datetime_seconds()
    dict_car["creator_id"] = str(userLogged.id)
        
    res = await connection.cars.insert_one(dict_car)
    id = res.inserted_id
    await connection.cars.update_one({"_id": ObjectId(id)}, {"$set": {"id":str(id)}})
    cardb = await connection.cars.find_one({"_id": id})
    return cardb


async def get_all_cars_controller(userLogged: User,search:str):
    search_regex = Regex(search, "i")  # Expresión regular para buscar parcialmente en strings

    # Pipeline de agregación para buscar en múltiples campos, incluyendo la conversión de números a string
    pipeline = [
        {
            "$addFields": {
                "year_str": {"$toString": "$year"},  # Convertir 'id_number' a string
                "thingspeak_id_str": {"$toString": "$thingspeak_id"}  # Opcional: convertir otros campos numéricos si es necesario
            }
        },
        {
            "$match": {
                "$or": [
                    {"name": search_regex},
                    {"plate": search_regex},
                    {"make": search_regex},
                    {"model": search_regex},
                    {"thingspeak_id_str": search_regex},
                    {"year_str": search_regex}
                ]
            }
        },
        {
            "$sort": {"name": 1}
        }
    ]
    #cars_async = connection.cars.find()
    cars = []

    if search != "":
        async for document in connection.cars.aggregate(pipeline):
            cars.append(document)
    else:
        cars_async = connection.cars.find().sort("name")
        async for document in cars_async:
            cars.append(document)
    return cars
    
async def get_car_controller(id: str,userLogged: User):
    vrf = await verify_car_id(id)    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    return await connection.cars.find_one({"_id": ObjectId(id)})


async def get_car_data(vehicle_id: int,amount: int,):
    url = f'https://api.thingspeak.com/channels/{vehicle_id}/feeds.json'
    payload = {"results":amount}
    response = requests.get(url, params=payload)
    
    response_json = response.json()
    cardata_list = []
    for i in response_json["feeds"]:
        data = {
            "date": i["created_at"],
            "fuel": i["field1"],
            "latitude": i["field3"],
            "longitude": i["field2"],
            "speed": i["field4"],
        }
        cardata_list.append(data)
    return cardata_list


async def get_car_map_controller(id: str,userLogged: User):
    actual_hour = get_current_time_in_bolivia_seconds()
    actual_weekday = get_current_weekday_in_bolivia()
    vrf = await verify_car_id(id)    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    car = await connection.cars.find_one({"_id": ObjectId(id)})
    carDataBase = {
        "_id": id,
        "name": car["name"],
        "plate": car["plate"],
        "make": car["make"],
        "model": car["model"],
        "year": car["year"],
        "thingspeak_id": car["thingspeak_id"],
        "full_name": f'{car["make"]} {car["model"]} {str(car["year"])} {car["plate"]}',
        "teacher_name": "",
        "longitude": "",
        "latitude": "",
        "fuel": "",
        "speed": "",
        "state": "",
        "zone": "",
        "is_working": "",
        "teacher_id": "",
    }

    schedules_async = connection.schedules.find({
        "$and": [
            { "car_id":car["id"] },
            { "day":actual_weekday}
        ]
    })
    schedules = []
    async for document in schedules_async:
        schedules.append(document)

    if not schedules:
        return carDataBase
    
    current_schedule={}
    for schedule in schedules:
        if actual_hour <= (schedule["hour"] + 3600) and actual_hour >= (schedule["hour"]):
            current_schedule = schedule

    teacher_request = {}
    if not current_schedule:
        car["teacher_name"] = ""
        car["teacher_id"] = ""
        car["is_working"] = ""
        #return carDataBase
    else:
        teacher = await connection.users.find_one({"id":current_schedule["teacher_id"]})
        car["teacher_name"] = teacher["first_name"] + " " + teacher["father_last_name"]
        car["teacher_id"]=teacher["id"]
        car["is_working"] = "Y"

    


    car_data = await get_car_data(car["thingspeak_id"],1)
    car["longitude"] = float(car_data[0]["longitude"])
    car["latitude"] = float(car_data[0]["latitude"])
    car["speed"] = float(car_data[0]["speed"])
    car["fuel"] = float(car_data[0]["fuel"])
    car["full_name"] = car["make"] + " " + car["model"]  + " " + str(car["year"])  + " " + car["plate"]
    car["last_time"] = convert_to_bolivia_time(car_data[0]["date"])
    


    isZone = is_point_in_polygon(car["longitude"],car["latitude"])
    if isZone:
        car["zone"]="Dentro de zona"
    else:
        car["zone"]="Fuera de zona"

    fecha_iso = car_data[0]["date"]
    isActive = is_within_last_minute(fecha_iso)

    if isActive:
        car["state"]="Activo"
    else:
        car["state"]="Inactivo"  
    
    return car



async def update_car_controller(id: str,car: UpdateCar, userLogged: User):
    vrf = await verify_car_id(id)    
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )

    original_car = await connection.cars.find_one({"_id":ObjectId(id)})
    dict_original_car = dict(original_car)
    dict_car = dict(car)
    vrf = {}
    update_car = {}
    for key, value in dict_car.items():
        if (value != None):
            update_car[key] = value
    
    vrf = verify_creator_rol(userLogged)
    if (not vrf["response"]):
        raise HTTPException(
            status_code = 403, 
            detail = vrf["detail"]
        )
    
    if("creation_date_inseconds" in update_car):
        raise HTTPException(
            status_code = 403, 
            detail = "Creation date can not bet modified"
        )
    
    if("creator_id" in update_car):
        raise HTTPException(
            status_code = 403, 
            detail = "Creator can not bet modified"
        )

    if("plate" in update_car):
        vrf = await verify_plate(update_car["plate"])    
        if (not vrf["response"]):
            raise HTTPException(
                status_code = 403, 
                detail = vrf["detail"]
            )  

    
    await connection.cars.update_one(
            {"_id": ObjectId(id)}, {"$set": update_car})
    
    return await connection.cars.find_one({"_id": ObjectId(id)})

async def delete_car_controller(id: str,userLogged: User):
    vrf = await verify_car_id(id)
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
    
    await connection.cars.delete_one({"_id": ObjectId(id)})

async def softdelete_car_controller(id: str,userLogged: User):
    vrf = await verify_car_id(id)    
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
    
    await connection.cars.update_one(
            {"_id": ObjectId(id)}, {"$set": {"deleted":True}})