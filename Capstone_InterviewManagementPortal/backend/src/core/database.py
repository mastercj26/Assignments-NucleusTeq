from pymongo import MongoClient
from src.core.config import settings

class Database:
    client: MongoClient = None
    db = None

    @classmethod
    def connect(cls):
        if cls.client is None:
            cls.client = MongoClient(settings.MONGO_URI)
            cls.db = cls.client[settings.DB_NAME]
            print("Connected to MongoDB")
        return cls.db

    @classmethod
    def get_collection(cls, name: str):
        db = cls.connect()
        return db[name]

# Initialize connection on import
Database.connect()