from fastapi import (
    APIRouter, Response, Depends
)
from schemas.cardata import carDataEntity,carDatasEntity
from models.user import User
from models.cardata import (
    CarData,
    UpdateCarData
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
import requests
# from controllers.cardata import (
#     create_cardata_controller,
#     get_all_cardatas_controller,
#     get_cardata_controller,
#     update_cardata_controller,
#     delete_cardata_controller,
#     softdelete_cardata_controller
# )

cardata = APIRouter(prefix="/cardatas", tags=["CarData"])
oauth2_scheme = OAuth2PasswordBearer("/login")
# @cardata.get('/', response_model=list[CarData])
#async def get_all_cardatas(amount: int, userLogged: User = Depends(get_user_disabled_current)):
@cardata.get('/')
async def get_all_cardatas(amount: int, vehicle_id: int,userLogged: User = Depends(get_user_disabled_current)):
    url = f'https://api.thingspeak.com/channels/{vehicle_id}/feeds.json'
    payload = {"results":amount}
    response = requests.get(url, params=payload)

    response_json = response.json()
    #print(response_json["feeds"])
    cardata_list = []
    for i in response_json["feeds"]:
        data = {
            "date": i["created_at"],
            "fuel": i["field1"],
            "latitude": i["field3"],
            "longitude": i["field2"],
            "speed": i["field4"],
        }
        print("---")
        print(f'Fecha: {i["created_at"]}', "\n")
        print(f'Combustible: {i["field1"]} L', "\n")
        print(f'Latitud: {i["field3"]}', "\n")
        print(f'Longitud: {i["field2"]}', "\n")
        print(f'Velocidad: {i["field4"]} Km/h', "\n")
        cardata_list.append(data)
    return cardata_list