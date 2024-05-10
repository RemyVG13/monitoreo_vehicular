from fastapi import (
    APIRouter, Response, Depends
)
from schemas.schedule import scheduleEntity,schedulesEntity
from schemas.schedule_detail import scheduleDetailEntity,schedulesDetailEntity
from models.user import User
from models.schedule import (
    Schedule,
    UpdateSchedule
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
from controllers.schedule import (
    create_schedule_controller,
    get_all_schedules_controller,
    get_schedule_controller,
    update_schedule_controller,
    delete_schedule_controller,
    softdelete_schedule_controller,
    get_detail_schedules_controller
)

schedule = APIRouter(prefix="/schedules", tags=["Schedule"])
oauth2_scheme = OAuth2PasswordBearer("/login")

@schedule.get('/', response_model=list[Schedule])
async def get_all_schedules(userLogged: User = Depends(get_user_disabled_current),search: str=""):
    schedules = await get_all_schedules_controller(userLogged,search)
    return schedulesEntity(schedules)

@schedule.get('/detail')
async def get_all_schedules_with_detail(userLogged: User = Depends(get_user_disabled_current),search: str=""):
    schedules = await get_detail_schedules_controller(userLogged,search)
    print("schedules")
    print(schedules)
    return schedulesDetailEntity(schedules)

@schedule.post('/', response_model=Schedule)
async def create_schedule(schedule: Schedule, userLogged: User = Depends(get_user_disabled_current)):
    schedulejson = await create_schedule_controller(schedule,userLogged)
    return scheduleEntity(dict(schedulejson))

@schedule.get('/{id}')
async def get_schedule(id: str,userLogged: User = Depends(get_user_disabled_current)):
    schedulejson = await get_schedule_controller(id,userLogged)
    return scheduleEntity(schedulejson)

@schedule.put('/{id}')
async def update_schedule(id: str, update_schedule: UpdateSchedule,userLogged: User = Depends(get_user_disabled_current)):
    print(update_schedule)
    schedulejson = await update_schedule_controller(id,update_schedule,userLogged) 
    return scheduleEntity(schedulejson)

@schedule.delete('/{id}')
async def delete_schedule(id: str, userLogged: User = Depends(get_user_disabled_current)):
    await delete_schedule_controller(id,userLogged)
    return Response(status_code=HTTP_204_NO_CONTENT)

@schedule.put('/softdelete/{id}')
async def softdelete_schedule(id: str, userLogged: User = Depends(get_user_disabled_current)):
    await softdelete_schedule_controller(id,userLogged)
    return Response(status_code=HTTP_204_NO_CONTENT)