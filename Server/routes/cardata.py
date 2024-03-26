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

import requests



# @cardata.get('/', response_model=list[CarData])
#async def get_all_cardatas(amount: int, userLogged: User = Depends(get_user_disabled_current)):
@cardata.get('/')
async def get_all_cardatas(amount: int, userLogged: User = Depends(get_user_disabled_current)):
    
    # The API endpoint
    url = "https://api.thingspeak.com/channels/2425622/feeds.json"

    # GET POST https://api.thingspeak.com/update?api_key=E43NHEZK74CHN9HG&field1=13&field3=-17.396740&field2=-66.317620&field4=15
    # GET all channel https://api.thingspeak.com/channels/2425622/feeds.json?results=0

    # Adding a payload
    payload = {"results":amount}

    # A get request to the API
    response = requests.get(url, params=payload)

    # Print the response
    response_json = response.json()
    print(response_json["feeds"])
    for i in response_json["feeds"]:
        print("---")
        # print(i, "\n")created_at
        print(f'Fecha: {i["created_at"]}', "\n")
        print(f'Combustible: {i["field1"]} L', "\n")
        print(f'Latitud: {i["field3"]}', "\n")
        print(f'Longitud: {i["field2"]}', "\n")
        print(f'Velocidad: {i["field4"]} Km/h', "\n")

    return {"response":"test"}
    #cardatas = await get_all_cardatas_controller(userLogged)
    #return cardatasEntity(cardatas)

# @cardata.get('/{id}')
# async def get_cardata(id: str,userLogged: User = Depends(get_user_disabled_current)):
#     cardatajson = await get_cardata_controller(id,userLogged)
#     return cardataEntity(cardatajson)

# @cardata.post('/', response_model=CarData)
# async def create_cardata(cardata: CarData, userLogged: User = Depends(get_user_disabled_current)):
#     cardatajson = await create_cardata_controller(cardata,userLogged)
#     return cardataEntity(dict(cardatajson))

# @cardata.put('/{id}')
# async def update_cardata(id: str, update_cardata: UpdateCarData,userLogged: User = Depends(get_user_disabled_current)):
#     cardatajson = await update_cardata_controller(id,update_cardata,userLogged) 
#     return cardataEntity(cardatajson)

# @cardata.delete('/{id}')
# async def delete_cardata(id: str, userLogged: User = Depends(get_user_disabled_current)):
#     await delete_cardata_controller(id,userLogged)
#     return Response(status_code=HTTP_204_NO_CONTENT)

# @cardata.put('/softdelete/{id}')
# async def softdelete_cardata(id: str, userLogged: User = Depends(get_user_disabled_current)):
#     await softdelete_cardata_controller(id,userLogged)
#     return Response(status_code=HTTP_204_NO_CONTENT)