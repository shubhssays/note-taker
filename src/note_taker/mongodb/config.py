from pymongo import MongoClient
from pymongo.database import Database
from note_taker.utils.settings import settings

class MongoDB:
    def __init__(self):
        self.client = MongoClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=5000,
        )

        self._db:Database = self.client[settings.MONGODB_DATABASE]

    def connect(self):
        try:
            self.client.admin.command("ping")
            print("MongoDB connected successfully")
        except Exception as exc:
            print(f"MongoDB connection failed: {exc}")
            raise    


    @property
    def db(self) -> Database:
        return self._db

mongoDB = MongoDB()