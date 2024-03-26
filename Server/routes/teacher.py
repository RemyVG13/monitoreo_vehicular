from fastapi import (
    APIRouter, Response, Depends
)
from schemas.user import userEntity,usersEntity
from models.user import (
    User,Teacher,
    UpdateTeacher
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
from controllers.teacher import (
    create_teacher_controller,
    get_all_teachers_controller,
    get_teacher_controller,
    update_teacher_controller,
    delete_teacher_controller,
    softdelete_teacher_controller
)

teacher = APIRouter(prefix="/teachers", tags=["Teacher"])
oauth2_scheme = OAuth2PasswordBearer("/login")

@teacher.get('/', response_model=list[Teacher])
async def get_all_teachers(userLogged: User = Depends(get_user_disabled_current)):
    teachers = await get_all_teachers_controller(userLogged)
    return usersEntity(teachers)

@teacher.post('/', response_model=Teacher)
async def create_teacher(teacher: Teacher, userLogged: User = Depends(get_user_disabled_current)):
    teacherjson = await create_teacher_controller(teacher,userLogged)
    return userEntity(dict(teacherjson))

@teacher.get('/{id}')
async def get_teacher(id: str,userLogged: User = Depends(get_user_disabled_current)):
    teacherjson = await get_teacher_controller(id,userLogged)
    return userEntity(teacherjson)

@teacher.put('/{id}')
async def update_teacher(id: str, update_teacher: UpdateTeacher,userLogged: User = Depends(get_user_disabled_current)):
    teacherjson = await update_teacher_controller(id,update_teacher,userLogged) 
    return userEntity(teacherjson)

@teacher.delete('/{id}')
async def delete_teacher(id: str, userLogged: User = Depends(get_user_disabled_current)):
    await delete_teacher_controller(id,userLogged)
    return Response(status_code=HTTP_204_NO_CONTENT)

@teacher.put('/softdelete/{id}')
async def softdelete_teacher(id: str, userLogged: User = Depends(get_user_disabled_current)):
    await softdelete_teacher_controller(id,userLogged)
    return Response(status_code=HTTP_204_NO_CONTENT)