from fastapi import FastAPI
from routes.user import user
from routes.teacher import teacher
from routes.schedule import schedule
from routes.car import car
from routes.cardata import cardata

from routes.authentication import auth
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://192.168.1.3",
    "http://192.168.1.12",
]

UVICORN_PORT = 8000
UVICORN_HOST = "192.168.1.3"
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

app.include_router(auth)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=UVICORN_HOST, port=UVICORN_PORT)