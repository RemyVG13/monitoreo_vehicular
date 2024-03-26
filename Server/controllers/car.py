from models.user import User, Roles
from config.db import connection
from passlib.context import CryptContext
from fastapi import HTTPException
from models.car import Car, UpdateCar
from scripts.time import bolivia_datetime_seconds
from bson import ObjectId

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

async def verify_car_id(id: str):
    res_id = await connection.cars.find_one({"_id":ObjectId(id)})
    if res_id == None:
        return  {"response": False, "detail": "Car does not exist"}
    return {"response": True, "detail": "Ok"}

async def verify_plate(id: str):
    res_id = await connection.cars.find_one({"_id":ObjectId(id)})
    if res_id == None:
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

async def get_all_cars_controller(userLogged: User):
    cars_async = connection.cars.find()
    cars = []
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