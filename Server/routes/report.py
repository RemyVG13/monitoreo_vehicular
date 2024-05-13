from fastapi import (
    APIRouter, Response, Depends
)

from models.user import User

from bson import ObjectId
from starlette.status import (
    HTTP_204_NO_CONTENT
)
from fastapi.security import (
    OAuth2PasswordBearer
)
from typing import Annotated
from routes.authentication import get_user_disabled_current

from controllers.report import (
    get_report_controller
)



report = APIRouter(prefix="/reports", tags=["report"])
oauth2_scheme = OAuth2PasswordBearer("/login")

@report.get('/')
async def get_all_reports(userLogged: User = Depends(get_user_disabled_current),car_id: str="", start_date:str="", end_date:str="", period:str="", report_type:str=""):
    reports = await get_report_controller(userLogged,car_id, start_date, end_date, period, report_type)

    return reports

