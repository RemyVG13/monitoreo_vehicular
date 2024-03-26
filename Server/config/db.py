from pymongo import MongoClient
import motor.motor_asyncio
DB_HOSTNAME = "127.0.0.1"
DB_PORT = 27017
DB_NAME = "local_general_motors"
client = motor.motor_asyncio.AsyncIOMotorClient(DB_HOSTNAME,DB_PORT)
connection = client[DB_NAME]
#conn = MongoClient(DB_HOSTNAME,DB_PORT)
#connection = conn[DB_NAME]