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
        
    async def get_user(self, user_id: int):
        user = await self.users.find_one({"_id": user_id})
        if not user:
            user = {
                "_id": user_id,
                "games_played": 0,
                "games_won": 0,
                "total_wealth_earned": 0,
                "bankruptcies": 0
            }
            await self.users.insert_one(user)
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

try:
    db = Database(config.MONGO_DB_URI, "BusinessGameBot")
    logger.info("Connected to MongoDB successfully!")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    db = None
