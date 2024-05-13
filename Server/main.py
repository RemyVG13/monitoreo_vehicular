from fastapi import FastAPI
from routes.user import user
from routes.teacher import teacher
from routes.schedule import schedule
from routes.car import car
from routes.cardata import cardata
from routes.alarm import alarm

from routes.authentication import auth
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://192.168.1.3",
    "http://192.168.1.12",
]


import sys
import os

UVICORN_PORT = 8000
UVICORN_HOST = "192.168.1.14"
# Detectar el sistema operativo
print(sys.platform)
if sys.platform.startswith('win'):
    # Configuraciones para Windows
    UVICORN_HOST = "localhost"
    UVICORN_PORT = 8000
else:
    # Configuraciones para Unix/Linux
    UVICORN_PORT = 8000
    UVICORN_HOST = "ec2-18-226-164-75.us-east-2.compute.amazonaws.com"


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(user)
app.include_router(teacher)
app.include_router(schedule)
app.include_router(car)
app.include_router(cardata)
app.include_router(alarm)

app.include_router(auth)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=UVICORN_HOST, port=UVICORN_PORT)
