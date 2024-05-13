from models.user import User, Roles
from config.db import connection
from passlib.context import CryptContext
from fastapi import HTTPException
from scripts.time import (bolivia_datetime_seconds,
                          convert_to_bolivia_time,
                          add_time_to_date
                          )
from bson import ObjectId
from bson.regex import Regex
import requests
import math

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 


def verify_getter_rol(getter: User):
    if ( (getter.rol != Roles.ADMIN.value) and (getter.rol != Roles.SUPERADMIN.value) and (getter.rol != Roles.TEACHER.value)):
        return  {"response": False, "detail": f'User {getter.first_name} does not have enough privileges'}
    return {"response": True, "detail": "Ok"}

def calculate_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371 * c
    
    return distance


#CRUD functions
async def get_report_controller(userLogged: User,cars_id: str, start_date:str, end_date:str, period:str, report_type:str):
    reports = {
        "car_name":"",
        "report_type":"",
        "report":[]
    }
    car = await connection.cars.find_one({"_id": ObjectId(cars_id)})
    reports["car_name"] = car["name"]
    reports["report_type"] = report_type
    if report_type == "Combustible":
        fuel_report = []
        url_fuel = f'https://api.thingspeak.com/channels/{car["thingspeak_id"]}/fields/1.json'
        payload = {
            "start":start_date,
            "end":end_date
            }
        response_fuel = requests.get(url_fuel, params=payload)
        response_fuel_json = response_fuel.json()
        i = 0
        temp_start_date = start_date
        fuel_consume = 0
        while i < len(response_fuel_json["feeds"]):
            j=0
            date_to_append = convert_to_bolivia_time(response_fuel_json["feeds"][i]["created_at"])
            fuel_report.append([date_to_append,fuel_consume])
            temp_url_fuel = f'https://api.thingspeak.com/channels/{car["thingspeak_id"]}/fields/1.json'
            payload = {
                "start":temp_start_date,
                }
            match period:
                case "Hora":
                    payload["end"] = add_time_to_date(temp_start_date,add_hours=1)
                case "Día":
                    payload["end"] = add_time_to_date(temp_start_date,add_days=1)
                case "Semana":
                    payload["end"] = add_time_to_date(temp_start_date,add_weeks=1)
                case "Mes":
                    payload["end"] = add_time_to_date(temp_start_date,add_months=1)
                case "Año":
                    payload["end"] = add_time_to_date(temp_start_date,add_years=1)
                case _:
                    payload["end"] = add_time_to_date(temp_start_date,add_days=1)
            
            
            temp_response_fuel = requests.get(temp_url_fuel, params=payload)
            temp_response_fuel_json = temp_response_fuel.json()
            
            while j < len(temp_response_fuel_json["feeds"]) - 1:
                fuel1 = float(temp_response_fuel_json["feeds"][j]["field1"])
                fuel2 = float(temp_response_fuel_json["feeds"][j+1]["field1"])
                if fuel1 and fuel2:
                    fuel_consume = fuel_consume + (fuel1-fuel2)
                j=j+1
                i=i+1

            temp_start_date = payload["end"] 
            i=i+1
            print(fuel_report)

        reports["report"] = fuel_report

    if report_type == "Distancia":
        distance_report = []
        
        url_longitude = f'https://api.thingspeak.com/channels/{car["thingspeak_id"]}/fields/2.json'
        url_latitude = f'https://api.thingspeak.com/channels/{car["thingspeak_id"]}/fields/3.json'
        payload = {"start":start_date,
                "end":end_date
                }
        response_longitude = requests.get(url_longitude, params=payload)
        response_latitude = requests.get(url_latitude, params=payload)
        response_longitude_json = response_longitude.json()
        response_latitude_json = response_latitude.json()

        i = 0
        temp_start_date = start_date
        distance = 0
        while i < len(response_longitude_json["feeds"]):
            j=0
            temp_url_longitude = f'https://api.thingspeak.com/channels/{car["thingspeak_id"]}/fields/2.json'
            temp_url_latitude = f'https://api.thingspeak.com/channels/{car["thingspeak_id"]}/fields/3.json'
            payload = {
                "start":temp_start_date,
                }
            match period:
                case "Hora":
                    payload["end"] = add_time_to_date(temp_start_date,add_hours=1)
                case "Día":
                    payload["end"] = add_time_to_date(temp_start_date,add_days=1)
                case "Semana":
                    payload["end"] = add_time_to_date(temp_start_date,add_weeks=1)
                case "Mes":
                    payload["end"] = add_time_to_date(temp_start_date,add_months=1)
                case "Año":
                    payload["end"] = add_time_to_date(temp_start_date,add_years=1)
                case _:
                    payload["end"] = add_time_to_date(temp_start_date,add_days=1)
            
            temp_response_longitude = requests.get(temp_url_longitude, params=payload)
            temp_response_longitude_json = temp_response_longitude.json()
            
            temp_response_latitude = requests.get(temp_url_latitude, params=payload)
            temp_response_latitude_json = temp_response_latitude.json()
            date_to_append = ""
            while j < len(temp_response_latitude_json["feeds"]) - 1:
                print("distancej")
                print(distance)
                if temp_response_latitude_json["feeds"][j]["field3"] and temp_response_longitude_json["feeds"][j]["field2"] and temp_response_latitude_json["feeds"][j+1]["field3"] and temp_response_longitude_json["feeds"][j+1]["field2"]:

                    lat1 = float(temp_response_latitude_json["feeds"][j]["field3"])
                    lon1 = float(temp_response_longitude_json["feeds"][j]["field2"])

                    lat2 = float(temp_response_latitude_json["feeds"][j+1]["field3"])
                    lon2 = float(temp_response_longitude_json["feeds"][j+1]["field2"])

                    if lat1 and lon1 and lat1 and lat2:
                        distance = distance + calculate_distance( lat1,lon1,lat2,lon2)
                        
                j=j+1
                i=i+1
            date_to_append = convert_to_bolivia_time(temp_start_date)
                
            
            distance_report.append([date_to_append,round(distance,2)])
            temp_start_date = payload["end"] 
            i=i+1
            #print(distance_report)

        reports["report"] = distance_report

    return reports

