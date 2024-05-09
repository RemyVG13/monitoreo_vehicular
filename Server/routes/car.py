from fastapi import (
    APIRouter, Response, Depends
)
from schemas.car import carEntity,carsEntity
from models.user import User
from models.car import (
    Car,
    UpdateCar
)
from bson import ObjectId
from starlette.status import (
    HTTP_204_NO_CONTENT
)
from fastapi.security import (
    OAuth2PasswordBearer
)
from typing import Annotated
from routes.authentication import get_user_disabled_current
from controllers.car import (
    create_car_controller,
    get_all_cars_controller,
    get_car_controller,
    update_car_controller,
    delete_car_controller,
    softdelete_car_controller
)

car = APIRouter(prefix="/cars", tags=["Car"])
oauth2_scheme = OAuth2PasswordBearer("/login")

@car.get('/', response_model=list[Car])
async def get_all_cars(userLogged: User = Depends(get_user_disabled_current),search: str=""):
    cars = await get_all_cars_controller(userLogged,search)
    return carsEntity(cars)

@car.post('/', response_model=Car)
async def create_car(car: Car, userLogged: User = Depends(get_user_disabled_current)):
    carjson = await create_car_controller(car,userLogged)
    return carEntity(dict(carjson))

@car.get('/{id}')
async def get_car(id: str,userLogged: User = Depends(get_user_disabled_current)):
    carjson = await get_car_controller(id,userLogged)
    return carEntity(carjson)

@car.put('/{id}')
async def update_car(id: str, update_car: UpdateCar,userLogged: User = Depends(get_user_disabled_current)):
    carjson = await update_car_controller(id,update_car,userLogged) 
    return carEntity(carjson)

@car.delete('/{id}')
async def delete_car(id: str, userLogged: User = Depends(get_user_disabled_current)):
    await delete_car_controller(id,userLogged)
    return Response(status_code=HTTP_204_NO_CONTENT)

@car.put('/softdelete/{id}')
async def softdelete_car(id: str, userLogged: User = Depends(get_user_disabled_current)):
    await softdelete_car_controller(id,userLogged)
    return Response(status_code=HTTP_204_NO_CONTENT)