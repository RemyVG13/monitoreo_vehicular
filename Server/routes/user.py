from fastapi import APIRouter, Response, status, Depends, Header
from config.db import connection
from schemas.user import userEntity,usersEntity
from models.user import User,Teacher,Admin,Superadmin
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_200_OK
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from routes.authentication import get_user_disabled_current
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
user = APIRouter(prefix="/users", tags=["User"])
oauth2_scheme = OAuth2PasswordBearer("/login")



@user.get('/', response_model=list[User])
async def find_all_users(userLogged: User = Depends(get_user_disabled_current)):
    users = await connection.users.find()
    return Response(status_code=HTTP_200_OK, content=usersEntity(users))

@user.post('/user')
async def create_user(user: User):
    dict_user = dict(user)
    dict_user["password"] = password_context.hash(dict_user["password"])
    res = await connection.users.insert_one(dict_user)
    id = res.inserted_id
    await connection.users.update_one({"_id": ObjectId(id)}, {"$set": {"id":str(id)}})
    userdb = await connection.users.find_one({"_id": id})
    return userEntity(userdb)

# @user.post('/', response_model=User)
# async def create_student(user: User, user_agent: Annotated[str | None, Header()] = None):
#     new_user = dict(user)
#     new_user["password"] = sha256_crypt.hash(new_user["password"])
#     id = await connection.users.insert_one(new_user).inserted_id
#     await connection.users.update_one({"_id": ObjectId(id)}, {"$set": {"id":str(id)}})
#     user = await connection.users.find_one({"_id": id})
#     return userEntity(user)

@user.get('/{id}')
async def find_user(id: str,token: str = Depends(oauth2_scheme)):
    return userEntity(await connection.users.find_one({"_id": ObjectId(id)}))

@user.put('/{id}')
async def update_user(id: str, user: User = Depends(get_user_disabled_current)):
    await connection.users.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(user)})
    return userEntity(await connection.users.find_one({"_id": ObjectId(id)}))

@user.delete('/{id}')
async def delete_user(id: str, token: str = Depends(oauth2_scheme)):
    await connection.users.delete_one({"_id": ObjectId(id)})
    return Response(status_code=HTTP_204_NO_CONTENT)