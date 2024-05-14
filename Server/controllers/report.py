from models.user import User, Roles
from config.db import connection
from passlib.context import CryptContext
from scripts.time import (convert_to_bolivia_time,
                          add_time_to_date
                          )
from bson import ObjectId
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

import aiohttp
import asyncio
from datetime import datetime, timedelta
from bson import ObjectId
from typing import List

#CRUD functions
async def fetch(session, url, params):
    async with session.get(url, params=params) as response:
        return await response.json()

async def get_report_controller(userLogged: User, car_id: str, start_date: str, end_date: str, period: str, report_type: str):
    reports = {
        "car_name": "",
        "report_type": "",
        "report": []
    }
    car = await connection.cars.find_one({"_id": ObjectId(car_id)})
    reports["car_name"] = car["name"]
    reports["report_type"] = report_type

    async with aiohttp.ClientSession() as session:
        if report_type == "Combustible":
            fuel_report = []
            url_fuel = f'https://api.thingspeak.com/channels/{car["thingspeak_id"]}/fields/1.json'
            payload = {
                "start": start_date,
                "end": end_date
            }
            response_fuel_json = await fetch(session, url_fuel, params=payload)
            temp_start_date = start_date
            fuel_consume = 0

            tasks = []
            while temp_start_date < end_date:
                temp_url_fuel = f'https://api.thingspeak.com/channels/{car["thingspeak_id"]}/fields/1.json'
                payload = {"start": temp_start_date}
                payload["end"] = add_time_to_date(temp_start_date, period)

                tasks.append(fetch(session, temp_url_fuel, params=payload))
                temp_start_date = payload["end"]

            results = await asyncio.gather(*tasks)

            for result in results:
                if not result["feeds"]:
                    continue
                for j in range(len(result["feeds"]) - 1):
                    fuel1 = float(result["feeds"][j]["field1"])
                    fuel2 = float(result["feeds"][j + 1]["field1"])
                    if fuel1 and fuel2:
                        fuel_consume += (fuel1 - fuel2)
                date_to_append = convert_to_bolivia_time(result["feeds"][0]["created_at"])
                fuel_report.append([date_to_append, fuel_consume])

            reports["report"] = fuel_report

        if report_type == "Distancia":
            distance_report = []
            url_longitude = f'https://api.thingspeak.com/channels/{car["thingspeak_id"]}/fields/2.json'
            url_latitude = f'https://api.thingspeak.com/channels/{car["thingspeak_id"]}/fields/3.json'
            payload = {
                "start": start_date,
                "end": end_date
            }
            tasks_long = []
            tasks_lat = []
            temp_start_date = start_date
            distance = 0  # Inicialización de la variable distance

            while temp_start_date < end_date:
                temp_url_longitude = f'https://api.thingspeak.com/channels/{car["thingspeak_id"]}/fields/2.json'
                temp_url_latitude = f'https://api.thingspeak.com/channels/{car["thingspeak_id"]}/fields/3.json'
                payload = {"start": temp_start_date}
                payload["end"] = add_time_to_date(temp_start_date, period)

                tasks_long.append(fetch(session, temp_url_longitude, params=payload))
                tasks_lat.append(fetch(session, temp_url_latitude, params=payload))
                temp_start_date = payload["end"]

            results_long = await asyncio.gather(*tasks_long)
            results_lat = await asyncio.gather(*tasks_lat)

            for i in range(len(results_long)):
                temp_response_longitude_json = results_long[i]
                temp_response_latitude_json = results_lat[i]

                if not temp_response_longitude_json["feeds"] or not temp_response_latitude_json["feeds"]:
                    continue

                for j in range(len(temp_response_latitude_json["feeds"]) - 1):
                    if temp_response_latitude_json["feeds"][j]["field3"] and temp_response_longitude_json["feeds"][j]["field2"] and temp_response_latitude_json["feeds"][j + 1]["field3"] and temp_response_longitude_json["feeds"][j + 1]["field2"]:
                        lat1 = float(temp_response_latitude_json["feeds"][j]["field3"])
                        lon1 = float(temp_response_longitude_json["feeds"][j]["field2"])
                        lat2 = float(temp_response_latitude_json["feeds"][j + 1]["field3"])
                        lon2 = float(temp_response_longitude_json["feeds"][j + 1]["field2"])

                        if lat1 and lon1 and lat2 and lon2:
                            distance += calculate_distance(lat1, lon1, lat2, lon2)
                date_to_append = convert_to_bolivia_time(temp_response_latitude_json["feeds"][0]["created_at"])
                distance_report.append([date_to_append, round(distance, 2)])
                
                temp_start_date = add_time_to_date(temp_start_date, period)  # Actualizar la fecha en cada iteración

            reports["report"] = distance_report

    return reports



def add_time_to_date(start_date: str, period: str) -> str:
    # Convertir la cadena de fecha y hora a un objeto datetime
    dt = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")
    
    # Agregar el tiempo según el período especificado
    if period == "Hora":
        dt += timedelta(hours=1)
    elif period == "Día":
        dt += timedelta(days=1)
    elif period == "Semana":
        dt += timedelta(weeks=1)
    elif period == "Mes":
        dt += timedelta(days=30)  # Aproximación de 30 días
    elif period == "Año":
        dt += timedelta(days=365)  # Aproximación de 365 días
    else:
        dt += timedelta(days=1)  # Período por defecto de un día
    
    # Convertir el objeto datetime de vuelta a una cadena en el formato ISO 8601 con 'Z'
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
