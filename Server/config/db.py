from pymongo import MongoClient
import motor.motor_asyncio
DB_HOSTNAME = "127.0.0.1"
DB_PORT = 27017
DB_NAME = "local_general_motors"
#client = motor.motor_asyncio.AsyncIOMotorClient(DB_HOSTNAME,DB_PORT)
client = motor.motor_asyncio.AsyncIOMotorClient(r'mongodb://admindb:.admin*%2313@docdb-2024-03-21-20-56-59.cluster-cf46i8i6sywd.us-east-2.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=C%3A%5CMyPC%5Cmw_aws%5Cglobal-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false')
connection = client[DB_NAME]
#conn = MongoClient(DB_HOSTNAME,DB_PORT)
#connection = conn[DB_NAME]