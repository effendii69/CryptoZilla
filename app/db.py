from motor.motor_asyncio import AsyncIOMotorClient

mongo_url = "mongodb://localhost:27017"

client = AsyncIOMotorClient(mongo_url)

db = client.test
users_collection = db.users
instruments_collection = db.instruments
