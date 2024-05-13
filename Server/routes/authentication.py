from fastapi import APIRouter, Response, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user import User,Teacher,Admin,Superadmin,Roles
from models.token import LoginForm
from passlib.hash import sha256_crypt
from config.db import connection
from bson import ObjectId
from datetime import datetime, timedelta
from typing import Union
from jose import jwt, JWTError
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

SECRET_KEY = "9dfff41cd78ac6b2827c649cbca427e834a32a01ad0db806bbcabdbcd432e597"
ALGORITHM = "HS256"

auth = APIRouter(tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer("/login")

#Verify token in every request
async def get_user(username):
    userFound = await connection.users.find_one({"username": username})
    if userFound:
        if Roles.TEACHER.value == userFound["rol"]:
            return Teacher(**userFound)
        if Roles.ADMIN.value == userFound["rol"]:
            return Admin(**userFound)
        if Roles.SUPERADMIN.value == userFound["rol"]:
            return Superadmin(**userFound)
        return User(**userFound)
    return []

async def get_user_current(token: str = Depends(oauth2_scheme)):
    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        username = token_decode.get("sub")
        rol = token_decode.get("rol")
        if username == None:
            print("get_user_current => No username")
            raise HTTPException(
                status_code=401, 
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        if rol == None:
            print("get_user_current => No password")
            raise HTTPException(
                status_code=401, 
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except JWTError:
        print("get_user_current => JWTError")
        raise HTTPException(
            status_code=401, 
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user = await get_user(username)
    if not user:
        print("get_user_current => No User")
        raise HTTPException(
            status_code=401, 
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


async def get_user_disabled_current(user: User = Depends(get_user_current)):
    if user.disabled:
        raise HTTPException(
            status_code=400,
            detail="Inactive user"
        )
    return user

#LOGIN(Get Token)
async def create_token(data: dict, time_expire: Union[datetime,None] = None):
    data_copy = data.copy()
    if time_expire is None:
        expires = datetime.utcnow() + timedelta(minutes=15)
    else:
        expires = datetime.utcnow() + time_expire
    data_copy.update({"exp": expires})
    token_jwt = jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

async def verify_password(plane_password, hashed_password):
    return password_context.verify(plane_password, hashed_password)
    

async def authenticate_user(username, password):
    user = await get_user(username)
    if not user:
        print("authenticate_user => No User")
        raise HTTPException(status_code=401, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    if not await verify_password(password,user.password):
         print("authenticate_user => No password")
         raise HTTPException(status_code=401, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"}
                            )       
    return user

@auth.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(days=7)
    access_token_jwt = await create_token({"sub": user.username,"rol":user.rol,"user":dict(user)}, access_token_expires)
    return {
        "access_token": access_token_jwt,
        "token_type": "bearer"
    }
