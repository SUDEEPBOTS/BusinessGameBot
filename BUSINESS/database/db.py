from motor.motor_asyncio import AsyncIOMotorClient
from BUSINESS import config
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, uri: str, database_name: str):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.users = self.db.users
        self.groups = self.db.groups
        
    async def get_user(self, user_id: int, name: str = "Unknown"):
        user = await self.users.find_one({"_id": user_id})
        if not user:
            user = {
                "_id": user_id,
                "name": name,
                "games_played": 0,
                "games_won": 0,
                "total_wealth_earned": 0,
                "bankruptcies": 0
            }
            await self.users.insert_one(user)
        elif "name" not in user or user["name"] != name:
            await self.update_user(user_id, name=name)
            user["name"] = name
        return user

    async def update_user(self, user_id: int, **kwargs):
        await self.users.update_one(
            {"_id": user_id},
            {"$set": kwargs},
            upsert=True
        )

    async def inc_user_stats(self, user_id: int, field: str, amount: int = 1):
        await self.users.update_one(
            {"_id": user_id},
            {"$inc": {field: amount}},
            upsert=True
        )
        
    async def add_group(self, chat_id: int):
        if not await self.groups.find_one({"_id": chat_id}):
            await self.groups.insert_one({"_id": chat_id})
            
    async def get_all_groups(self):
        cursor = self.groups.find({})
        return [g["_id"] for g in await cursor.to_list(length=None)]

try:
    db = Database(config.MONGO_DB_URI, "BusinessGameBot")
    logger.info("Connected to MongoDB successfully!")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    db = None
