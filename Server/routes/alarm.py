from fastapi import (
    APIRouter, Response, Depends
)
from schemas.alarm import alarmEntity,alarmsEntity
from models.user import User
from models.alarm import (
    Alarm,
    UpdateAlarm
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
from controllers.alarm import (
    create_geoalarm_controller,
    get_all_alarms_controller,
    create_fuelalarm_controller
)

alarm = APIRouter(prefix="/alarms", tags=["alarm"])
oauth2_scheme = OAuth2PasswordBearer("/login")

@alarm.get('/')
async def get_all_alarms(userLogged: User = Depends(get_user_disabled_current),search: str=""):
    alarms = await get_all_alarms_controller(userLogged,search)
    return alarmsEntity(alarms)

@alarm.post('/geo/')
async def create_geo_alarm(alarm: Alarm, userLogged: User = Depends(get_user_disabled_current)):
    alarmjson = await create_geoalarm_controller(alarm,userLogged)
    return alarmEntity(dict(alarmjson))

@alarm.post('/fuel/')
async def create_fuel_alarm(alarm: Alarm, userLogged: User = Depends(get_user_disabled_current)):
    alarmjson = await create_fuelalarm_controller(alarm,userLogged)
    return alarmEntity(dict(alarmjson))
