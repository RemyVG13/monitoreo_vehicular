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
    if updated_car.get("plate") is not None and updated_car.get("plate") != existing_car.get("plate"):
        updated_plate = updated_car.get("plate", existing_car.get("plate"))
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

'''
requests to thingspeak
1 = combustible
2 = longitud
3 = latitude
4 = velocidad
6 = geo alarma
7 = fuel alarma
GET https://api.thingspeak.com/update?api_key=E43NHEZK74CHN9HG&field1=43.8&field2=43.8&field1=43.8&field1=43.8&field1=43.8&field1=43.8
'''


async def get_car_history_controller(id:str,date_start:str,date_end:str):
    #https://api.thingspeak.com/channels/2425622/fields/3.json?start=2024-04-26T10:10:14Z&end=2024-04-26T10:20:46Z
    car = await connection.cars.find_one({"_id": ObjectId(id)})
    url_longitude = f'https://api.thingspeak.com/channels/{car["thingspeak_id"]}/fields/2.json'
    url_latitude = f'https://api.thingspeak.com/channels/{car["thingspeak_id"]}/fields/3.json'
    payload = {"start":date_start,
               "end":date_end
               }
    response_longitude = requests.get(url_longitude, params=payload)
    response_latitude = requests.get(url_latitude, params=payload)
    response_longitude_json = response_longitude.json()
    response_latitude_json = response_latitude.json()
    coords_list = []
    dates_list = []
    teacher_name_list = []
    i = 0
    print(url_longitude)
    print(response_longitude)
    print("response_longitude_json[feeds]")
    print(response_longitude_json)
    while i < len(response_longitude_json["feeds"]) :
        long = response_longitude_json["feeds"][i]["field2"]
        lat = response_latitude_json["feeds"][i]["field3"]
        coords = [float(lat),float(long)]
        coords_list.append(coords)

        dates_list.append(convert_to_bolivia_time(response_latitude_json["feeds"][i]["created_at"]))

        dates = iso_to_local_time(response_latitude_json["feeds"][i]["created_at"])
        schedules_async = connection.schedules.find({
            "$and": [
                { "car_id":car["id"] },
                { "day":dates["day"]}
            ]
        })
        teacher_name = "No hay instructor"
        schedules = []
        async for document in schedules_async:
            schedules.append(document)

        if not schedules:
            teacher_name = "No hay instructor"
        else:
            current_schedule={}
            for schedule in schedules:
                if dates["timestamp"] <= (schedule["hour"] + 3600) and dates["timestamp"] >= (schedule["hour"]):
                    current_schedule = schedule

            if not current_schedule:
                teacher_name = "No hay instructor"
                #return carDataBase
            else:
                teacher = await connection.users.find_one({"id":current_schedule["teacher_id"]})
                teacher_name = teacher["first_name"] + " " + teacher["father_last_name"]

        teacher_name_list.append(teacher_name)
        i=i+1
    history = {
        "coords_list": coords_list,
        "dates_list": dates_list,
        "teacher_name_list":teacher_name_list
    }
    return history



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
        "longitude": 0,
        "latitude":0,
        "fuel": 0,
        "speed": 0,
        "state": "",
        "zone": "",
        "is_working": "",
        "teacher_id": "",
        "last_time": "",
    }



    car_data = await get_car_data(car["thingspeak_id"],1)
    print("car_data||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    print(car_data)
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
        car["teacher_name"] = ""
    else:
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